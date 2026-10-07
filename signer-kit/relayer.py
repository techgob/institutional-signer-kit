"""Relayer con política restringida (pieza 2). Interfaz y formatos: docs/pieza2-interfaz.md.

El operador recibe la invocación que autorizó un rol (función de host y entradas firmadas), la
compara con la política, publica las entradas como XDR, firma como origen, paga y transmite. Cada
envío queda en comisiones.jsonl y cada rechazo en rechazos.jsonl, dentro de la carpeta de registro.

Uso: python signer-kit/relayer.py --politica politica.json --registro registro/ --operador <alias> solicitud.json
Imprime el resultado en JSON. Código de salida: 0 aceptada, 2 rechazada, 3 fallida en la red, 1 error.
"""
import argparse
import hashlib
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from stellar_sdk import xdr
from stellar_sdk.address import Address

FORMATO_FECHA = "%Y-%m-%dT%H:%M:%SZ"
CAMPOS_POLITICA = ("version", "red", "periodo_segundos", "vigencia_maxima_ledgers", "comision_maxima_stroops",
                   "permitidos", "roles")
CAMPOS_TRANSACCION = ("estado", "hash", "enlace", "transmite_y_paga", "comision_stroops", "ledger")
SALIDA = {"aceptada": 0, "rechazada": 2, "fallida": 3}


class Rechazo(Exception):
    def __init__(self, codigo: str, motivo: str, detalle: dict):
        super().__init__(motivo)
        self.codigo, self.motivo, self.detalle = codigo, motivo, detalle


class SimulacionFallida(Exception):
    """La red no pudo simular la invocación: firma inválida, nonce ya usado, contrato que falla."""


def entrada_invalida(razon: str, motivo: str, **detalle) -> Rechazo:
    return Rechazo("ENTRADA_INVALIDA", motivo, {"razon": razon, **detalle})


def credenciales(entrada: xdr.SorobanAuthorizationEntry):
    """Credenciales de dirección de la entrada, o None si autoriza la cuenta de origen (verifier/conformidad.py:30-32)."""
    c = entrada.credentials
    return c.address or c.address_v2 or (c.address_with_delegates and c.address_with_delegates.address_credentials)


def huella(texto: str) -> str:
    return hashlib.sha256(texto.encode()).hexdigest()


def huella_solicitud(solicitud) -> str:
    try:
        return huella("\n".join([solicitud["funcion_host"], *solicitud["entradas"]]))
    except (KeyError, TypeError):
        return huella(json.dumps(solicitud, sort_keys=True, default=str))


def validar_politica(politica: dict) -> None:
    faltan = [c for c in CAMPOS_POLITICA if c not in politica]
    if faltan:
        raise ValueError(f"a la política le faltan campos: {', '.join(faltan)}")
    if politica["version"] != 1:
        raise ValueError(f"versión de política no soportada: {politica['version']}")


def decodificar(solicitud):
    """Orden 1 de la sección 4: la forma de la solicitud, sin red."""
    entradas_xdr = solicitud.get("entradas") if isinstance(solicitud, dict) else None
    if (not isinstance(solicitud, dict) or solicitud.get("version") != 1
            or not isinstance(solicitud.get("funcion_host"), str)
            or not isinstance(entradas_xdr, list) or not entradas_xdr
            or not all(isinstance(e, str) for e in entradas_xdr)):
        raise entrada_invalida("formato", "La solicitud no tiene el formato de la versión 1")
    try:
        funcion_host = xdr.HostFunction.from_xdr(solicitud["funcion_host"])
        entradas = [xdr.SorobanAuthorizationEntry.from_xdr(e) for e in entradas_xdr]
    except Exception:  # el SDK lanza distintos tipos según dónde falle la lectura del XDR
        raise entrada_invalida("formato", "Un XDR de la solicitud no se puede leer")

    if funcion_host.type != xdr.HostFunctionType.HOST_FUNCTION_TYPE_INVOKE_CONTRACT:
        raise entrada_invalida("funcion_host_no_invocacion", "Solo se pagan invocaciones de contrato")
    invocacion = funcion_host.invoke_contract
    firmantes = [credenciales(e) for e in entradas]
    if any(c is None for c in firmantes):
        raise entrada_invalida("sin_autorizacion_de_rol",
                               "Una entrada no trae credenciales de dirección: autorizaría el operador, no el rol")
    try:
        roles = {Address.from_xdr_sc_address(c.address).address for c in firmantes}
        contrato = Address.from_xdr_sc_address(invocacion.contract_address).address
        funcion = invocacion.function_name.sc_symbol.decode()
    except ValueError:  # tipo de dirección que el SDK no convierte, o un nombre de función que no es texto
        raise entrada_invalida("formato", "Una dirección o el nombre de la función no se pueden leer")
    if len(roles) > 1:
        raise entrada_invalida("mas_de_un_rol", "Esta versión admite entradas de un solo rol")
    if any(e.root_invocation.function.contract_fn != invocacion for e in entradas):
        raise entrada_invalida("invocacion_distinta", "La invocación firmada no coincide con la función de host")
    if any(c.signature.type == xdr.SCValType.SCV_VOID for c in firmantes):
        raise entrada_invalida("sin_firma", "Una entrada no está firmada")

    vence = min(c.signature_expiration_ledger.uint32 for c in firmantes)
    return funcion_host, entradas, contrato, funcion, roles.pop(), vence


class Relayer:
    def __init__(self, politica: dict, registro: Path, red, reloj):
        validar_politica(politica)
        self.politica = politica
        self.registro = Path(registro)
        self.red = red
        self.reloj = reloj
        self.permitidas = {p["contrato"]: list(p["funciones"]) for p in politica["permitidos"]}

    def procesar(self, solicitud) -> dict:
        ahora = self.reloj()
        sha = huella_solicitud(solicitud)
        try:
            funcion_host, entradas, contrato, funcion, rol, vence = decodificar(solicitud)
        except Rechazo as r:
            return self._rechazar(r, ahora, sha, None, None, None)
        try:
            estimada = self._controlar(funcion_host, entradas, contrato, funcion, rol, vence, ahora)
        except Rechazo as r:
            return self._rechazar(r, ahora, sha, rol, contrato, funcion)
        return self._enviar(funcion_host, entradas, solicitud["entradas"], sha, contrato, funcion, rol, estimada, ahora)

    def _controlar(self, funcion_host, entradas, contrato, funcion, rol, vence, ahora) -> int:
        """Órdenes 2 a 8 de la sección 4. Devuelve la comisión estimada si la invocación pasa."""
        p = self.politica
        if contrato not in self.permitidas:
            raise Rechazo("CONTRATO_NO_PERMITIDO", f"El contrato {contrato} no está permitido", {"contrato": contrato})
        if funcion not in self.permitidas[contrato]:
            raise Rechazo("FUNCION_NO_PERMITIDA", f"La función {funcion} no está permitida para el contrato {contrato}",
                          {"contrato": contrato, "funcion": funcion, "permitidas": self.permitidas[contrato]})
        if rol not in p["roles"]:
            raise Rechazo("ROL_NO_PERMITIDO", f"El rol {rol} no está en la política", {"rol": rol})
        limites = p["roles"][rol]
        previas = self._comisiones_del_rol(rol, ahora)
        if len(previas) >= limites["max_solicitudes"]:
            raise Rechazo("LIMITE_DE_FRECUENCIA",
                          f"El rol ya envió {len(previas)} solicitudes en el período; el máximo es {limites['max_solicitudes']}",
                          {"solicitudes_en_periodo": len(previas), "max_solicitudes": limites["max_solicitudes"],
                           "periodo_segundos": p["periodo_segundos"]})

        vence_en = vence - self.red.ultimo_ledger()
        if vence_en <= 0:
            raise entrada_invalida("vencida", "La firma del rol ya venció", vence_en_ledgers=vence_en)
        if vence_en > p["vigencia_maxima_ledgers"]:
            raise entrada_invalida("vigencia_excesiva",
                                   f"La firma vence en {vence_en} ledgers; el máximo es {p['vigencia_maxima_ledgers']}",
                                   vence_en_ledgers=vence_en)

        try:
            estimada = self.red.estimar_comision(funcion_host, entradas)
        except SimulacionFallida as e:
            raise entrada_invalida("simulacion_fallida", "La red no pudo simular la invocación", mensaje=str(e))
        if estimada > p["comision_maxima_stroops"]:
            raise Rechazo("COMISION_EXCESIVA",
                          f"La comisión estimada ({estimada} stroops) supera el máximo por transacción",
                          {"comision_estimada_stroops": estimada, "comision_maxima_stroops": p["comision_maxima_stroops"]})
        consumido = sum(linea["comision_stroops"] or 0 for linea in previas)
        if consumido + estimada > limites["tope_stroops"]:
            raise Rechazo("TOPE_DE_GASTO",
                          f"El rol consumió {consumido} stroops en el período; con {estimada} más supera su tope",
                          {"consumido_stroops": consumido, "comision_estimada_stroops": estimada,
                           "tope_stroops": limites["tope_stroops"], "periodo_segundos": p["periodo_segundos"]})
        return estimada

    def _enviar(self, funcion_host, entradas, entradas_xdr, sha, contrato, funcion, rol, estimada, ahora) -> dict:
        xdr_publicado = f"publicadas/{sha}.xdr"
        (self.registro / "publicadas").mkdir(parents=True, exist_ok=True)
        (self.registro / xdr_publicado).write_text("\n".join(entradas_xdr))  # mismo formato que hu01.py:150

        resultado = self.red.transmitir(funcion_host, entradas)
        transaccion = {campo: resultado[campo] for campo in CAMPOS_TRANSACCION}
        self._agregar("comisiones.jsonl", {
            "fecha": ahora.strftime(FORMATO_FECHA), "rol": rol, "contrato": contrato, "funcion": funcion,
            "solicitud_sha256": sha, "entradas_sha256": [huella(e) for e in entradas_xdr],
            "xdr_publicado": xdr_publicado, "comision_estimada_stroops": estimada, **transaccion,
        })
        return {"estado": "aceptada" if transaccion["estado"] == "SUCCESS" else "fallida",
                "rol": rol, "contrato": contrato, "funcion": funcion, "xdr_publicado": xdr_publicado,
                "comision_estimada_stroops": estimada, "transaccion": transaccion}

    def _rechazar(self, r: Rechazo, ahora, sha, rol, contrato, funcion) -> dict:
        self._agregar("rechazos.jsonl", {
            "fecha": ahora.strftime(FORMATO_FECHA), "codigo": r.codigo, "motivo": r.motivo, "solicitud_sha256": sha,
            "rol": rol, "contrato": contrato, "funcion": funcion, "detalle": r.detalle,
        })
        return {"estado": "rechazada", "codigo": r.codigo, "motivo": r.motivo, "detalle": r.detalle}

    def _comisiones_del_rol(self, rol: str, ahora: datetime) -> list:
        ruta = self.registro / "comisiones.jsonl"
        if not ruta.exists():
            return []
        desde = ahora - timedelta(seconds=self.politica["periodo_segundos"])
        lineas = [json.loads(linea) for linea in ruta.read_text().splitlines() if linea.strip()]
        return [linea for linea in lineas if linea["rol"] == rol
                and datetime.strptime(linea["fecha"], FORMATO_FECHA).replace(tzinfo=timezone.utc) > desde]

    def _agregar(self, nombre: str, linea: dict) -> None:
        self.registro.mkdir(parents=True, exist_ok=True)
        with open(self.registro / nombre, "a", encoding="utf-8") as archivo:
            archivo.write(json.dumps(linea, ensure_ascii=False) + "\n")


class RedTestnet:
    """Testnet con la clave del operador leída de la CLI de Stellar (signer-kit/hu01.py:32-34)."""

    def __init__(self, alias_operador: str):
        import hu01  # solo aquí: el relayer y sus pruebas no necesitan red ni claves
        from stellar_sdk import SorobanServer

        self._hu01 = hu01
        self.server = SorobanServer(hu01.RPC)
        self.operador = hu01.clave(alias_operador)
        self._preparada = None

    def ultimo_ledger(self) -> int:
        return self.server.get_latest_ledger().sequence

    def estimar_comision(self, funcion_host, entradas) -> int:
        preparada = self._preparar(funcion_host, entradas)
        self._preparada = (self._clave(funcion_host, entradas), preparada)
        return preparada.transaction.fee

    def transmitir(self, funcion_host, entradas) -> dict:
        # Envía la misma transacción que se estimó: su comisión máxima es la que pasó la política.
        clave, preparada = self._preparada or (None, None)
        if clave != self._clave(funcion_host, entradas):
            preparada = self._preparar(funcion_host, entradas)
        self._preparada = None
        preparada.sign(self.operador)

        from stellar_sdk.soroban_rpc import SendTransactionStatus

        envio = self.server.send_transaction(preparada)
        if envio.status not in (SendTransactionStatus.PENDING, SendTransactionStatus.DUPLICATE):
            raise RuntimeError(f"la red no aceptó la transacción ({envio.status.value}): {envio.error_result_xdr}")
        res = self._hu01.esperar(self.server, envio.hash)
        cobrado = xdr.TransactionResult.from_xdr(res.result_xdr).fee_charged.int64 if res.result_xdr else None
        return {  # mismos campos que hu01.py:113-125
            "estado": res.status.value,
            "hash": res.transaction_hash,
            "enlace": self._hu01.EXPLORER + res.transaction_hash,
            "transmite_y_paga": self.operador.public_key,
            "comision_stroops": cobrado,
            "ledger": res.ledger,
        }

    def _preparar(self, funcion_host, entradas):
        """El operador es origen, las entradas firmadas van adjuntas y la red simula (hu01.py:96-99)."""
        from stellar_sdk import TransactionBuilder
        from stellar_sdk.exceptions import PrepareTransactionException
        from stellar_sdk.operation import InvokeHostFunction

        cuenta = self.server.load_account(self.operador.public_key)
        tx = (TransactionBuilder(cuenta, self._hu01.PASSPHRASE, base_fee=100)
              .append_operation(InvokeHostFunction(host_function=funcion_host, auth=entradas))
              .set_timeout(120)
              .build())
        try:
            return self.server.prepare_transaction(tx)
        except PrepareTransactionException as e:
            raise SimulacionFallida(str(e)) from e

    @staticmethod
    def _clave(funcion_host, entradas) -> tuple:
        return funcion_host.to_xdr(), tuple(e.to_xdr() for e in entradas)


class _Argumentos(argparse.ArgumentParser):
    def error(self, message):  # argparse sale con 2, que aquí significa "rechazada"
        self.print_usage(sys.stderr)
        print(f"error: {message}", file=sys.stderr)
        sys.exit(1)


def main(argv=None) -> int:
    parser = _Argumentos(description="Relayer con política restringida (pieza 2)")
    parser.add_argument("--politica", required=True, type=Path, help="archivo de política en JSON")
    parser.add_argument("--registro", required=True, type=Path, help="carpeta de comisiones, rechazos y XDR publicados")
    parser.add_argument("--operador", required=True, help="alias de la CLI de Stellar con la clave del operador")
    parser.add_argument("solicitud", type=Path, help="solicitud en JSON")
    args = parser.parse_args(argv)

    politica = json.loads(args.politica.read_text())
    validar_politica(politica)
    if politica["red"] != "testnet":
        raise ValueError(f"esta versión solo opera en testnet, no en {politica['red']}")
    solicitud = json.loads(args.solicitud.read_text())
    relayer = Relayer(politica, args.registro, RedTestnet(args.operador), lambda: datetime.now(timezone.utc))
    resultado = relayer.procesar(solicitud)
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
    return SALIDA[resultado["estado"]]


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # red caída, política inválida, clave inexistente: código 1
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)
