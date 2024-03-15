from dotenv import dotenv_values
import os

dicionario = dotenv_values()


if dicionario["TESTE"] == "3":
    print("nicess")
