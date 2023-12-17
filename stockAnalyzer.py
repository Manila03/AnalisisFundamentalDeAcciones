from ast import Str
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pyperclip
from tkinter.messagebox import showinfo
import yfinance as yf
import pandas as pd
import requests


tiempo_actual = time.time()
estructura_tiempo = time.localtime(tiempo_actual)

anio_actual = estructura_tiempo.tm_year


def analisis(accion):
    # Crear un objeto Ticker para la acción ingresada por el usuario
    "https://es.investing.com/equities/siderar-ratios"


    # Crear el objeto Ticker
    laAccion = yf.Ticker(accion)

    data = laAccion.info
    # precioActual = data['currentPrice']
    # print(data)

    # Obtener el historial de precios de la acción
    historial_precios = laAccion.history(period='max')
    # print(historial_precios)
    IS = laAccion.income_stmt
    BS = laAccion.balance_sheet
    CF = laAccion.cashflow
    cashflow = []
    for i in CF:
        FCF = CF[i]['Free Cash Flow']
        cashflow.append(FCF)
    TotalAssets = []
    CurrentAssets = []
    TotalLiabilities = []
    CurrentLiabilities = []
    for i in BS:
        TA = BS[i]['Total Assets']
        TotalAssets.append(TA)
        CA = BS[i]['Current Assets']
        CurrentAssets.append(CA)
        TL = BS[i]['Total Liabilities Net Minority Interest']
        TotalLiabilities.append(TL)
        CL = BS[i]['Current Liabilities']
        CurrentLiabilities.append(CL)
    NetIncome = []
    TotalIncome = []
    for i in IS:
        netCome = IS[i]['Net Income']
        totalCome = IS[i]['Total Revenue']
        NetIncome.append(netCome)
        TotalIncome.append(totalCome)

    RotacionDeActivos = str((NetIncome[0]) / (TotalAssets[0]))

    print(" \n ")
    # print(IS,BS,CF)
    
    lisDiferenciaTotal = []
    lisDiferenciaCurrent = []
    for i in range(len(TotalAssets)):
        DiffTotal = TotalAssets[i] - TotalLiabilities[i]
        DiffCurrent = CurrentAssets[i] - CurrentLiabilities[i]
        lisDiferenciaTotal.append(DiffTotal)
        lisDiferenciaCurrent.append(DiffCurrent)
    

    lisDiferenciaTotal.reverse()
    lisDiferenciaCurrent.reverse()
    PorcentualTotalGrowthList = []
    PorcentualCurrentGrowthList = []
    for i in range(4):
        if i <= 2:
            porcentajeTotal = str(round(((lisDiferenciaTotal[i+1] - lisDiferenciaTotal[i])/lisDiferenciaTotal[i])*100)) + "%"
            porcentajeCurrent =str(round(((lisDiferenciaCurrent[i+1] - lisDiferenciaCurrent[i])/lisDiferenciaCurrent[i])*100)) + "%"
            PorcentualTotalGrowthList.append(porcentajeTotal)
            PorcentualCurrentGrowthList.append(porcentajeCurrent)
            


    promedioDiffTotal = (sum(lisDiferenciaTotal)) / len(lisDiferenciaTotal)
    promedioDiffCurrent = (sum(lisDiferenciaCurrent)) / len(lisDiferenciaCurrent)

    sharesOutStanding = laAccion.get_shares_full(start="2022-01-01", end=None)

    # Asegúrate de seleccionar un valor específico de GrossProfit y sharesOutStanding antes de realizar la división
    ListaMargenIngTotales_IngNetos = []
    for i in range(4):
        MargenIngT_IngN = str(round((float(NetIncome[i]) / float(TotalIncome[i])) * 100)) + "%"
        ListaMargenIngTotales_IngNetos.append(MargenIngT_IngN)
    ListaMargenIngTotales_IngNetos.reverse()

    # BPA = ((GrossProfit[0]) / (sharesOutStanding[0]))
    # PEratio = round((precioActual)/(EPSlist[0]))
    PEratio = data['trailingPE']
    EnterpriseValueToEBITDA = data['enterpriseToEbitda']
    PriceToSales = data['priceToSalesTrailing12Months']
    PriceToBook = data['priceToBook']
    print(f"{accion}:          los años en los que esta expresado este analisis son de la forma: [ {anio_actual-1}, {anio_actual-2}, {anio_actual-3}, {anio_actual-4} ]")
    print("----------------------------------")
    print("El historial del margen de ganancias (ingrNetos / ingrTotales) son: ",ListaMargenIngTotales_IngNetos)
    print("\n")
    print("lista del porcentaje de crecimiento de la diferencia NO corriente entre activos y pasivos: ",PorcentualTotalGrowthList)
    print("\n")
    print("lista del porcentaje de crecimiento de la diferencia corriente entre activos y pasivos: ",PorcentualCurrentGrowthList)
    print("\n")       
    print("Price to Earnings Ratio (TTM): ", PEratio)
    print("\n")
    print("Enterprise Value / EBITDA: ", EnterpriseValueToEBITDA)
    print("\n")
    print("Price to Sales (TTM): ",PriceToSales)
    print("\n")
    print("Price to Book (ultimo trimestre): ",PriceToBook)
    print("\n")
    # ahora ya tenemos una lista con todos los simbolos de la competencia lo que haremos ahora sera analizar cada una y devolver los mismos datos que para la accion original
    return(PEratio, EnterpriseValueToEBITDA, PriceToSales, PriceToBook)
    





# Solicitar el símbolo de la acción al usuario
print("AVISO: Hay ciertas acciones del mercado argentino(MERVAL) que necesiten que se ingrese un '.BA' (sin espacios) luego del simbolo por cuestiones de la API que estamos usando")
print("\n")
stock = input("Símbolo de la acción a analizar: ")
numCompe = int(input("con cuantas empresas de la misma industria desea comparar esta accion? (luego le preguntaremos cuales): "))
competencia = []
for i in range(numCompe):
    simbComp = input("ingrese el simbolo de una empresa de la misma industria que nuestra acción: ")
    competencia.append(simbComp)

accionAAnalizar = analisis(stock)

print(accionAAnalizar)

listaListas = []
for i in range(numCompe):
    compStock = []
    datosDelStock = analisis(competencia[i])
    for j in range(4):
        compStock.append(datosDelStock[j])
    listaListas.append(compStock)
print(listaListas)

promedioPEratio = 0
promedioEnterpriseValueToEBITDA = 0
promedioPriceToSales = 0
promedioPriceToBook = 0

for i in (listaListas):
    promedioPEratio += i[0]
    promedioEnterpriseValueToEBITDA += i[1]
    promedioPriceToSales += i[2]
    promedioPriceToBook += i[3]

promedioPEratio/=(len(listaListas))
promedioEnterpriseValueToEBITDA/=(len(listaListas))
promedioPriceToSales/=(len(listaListas))
promedioPriceToBook/=(len(listaListas))

print("el promedio de Price/Earnings ratio de la industria es: ",promedioPEratio)
print("el promedio de EnterpriseValue/EBITDA ratio de la industria es: ",promedioEnterpriseValueToEBITDA) 
print("el promedio de Price/Sales ratio de la industria es: ",promedioPriceToSales) 
print("el promedio de Price/Book ratio de la industria es: ",promedioPriceToBook)  
print("\n")
print("\n")
print("recordemos que TTM significa que es un dato tomado de los ultimos 12 meses de la empresa")
print("\n")
print("El Price to Earnings(trailed): Un trailing P/E más alto puede indicar que el mercado tiene expectativas optimistas sobre el crecimiento futuro de las ganancias de la empresa, pero también podría indicar que la acción está sobrevalorada. Por otro lado, un trailing P/E más bajo podría sugerir que la acción podría estar infravalorada")
print("\n")
print("El Ev/Ebitda: Un bajo ratio EV/EBITDA puede indicar que la empresa está subvaluada en comparación con sus ganancias operativas. Sin embargo, es esencial considerar la industria y el ciclo de vida de la empresa al interpretar este ratio. Un ratio más bajo que el de la competencia podría sugerir que la empresa está relativamente infravalorada")
print("\n")
print("El Price to Sales: Es especialmente útil para empresas que no generan beneficios o tienen beneficios volátiles. Un P/S bajo puede indicar que la empresa está infravalorada en relación con sus ingresos, pero se debe comparar con empresas similares en la industria.")
print("\n")
print("El Price to Book: Un P/B inferior a 1 podría indicar que la acción se está vendiendo por debajo de su valor contable, lo que podría considerarse una señal de que la acción está infravalorada \n ademas Un P/B superior a 1 indica que el mercado está dispuesto a pagar un precio mayor que el valor contable de la empresa. Esto podría deberse a expectativas positivas sobre el crecimiento futuro de la empresa, la calidad de sus activos, o la perspectiva de ganancias")
print("\n")