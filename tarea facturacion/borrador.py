def decorador(func):
    def wrapper(*args, **kwargs):
        print("Antes de llamar a la función")
        resultado = func(*args, **kwargs)
        print("Después de llamar a la función")
        return resultado
    return wrapper

@decorador
def mi_funcion():
    print("Dentro de la función")

mi_funcion()
