from ast import Str
import time
from tkinter.messagebox import showinfo
import yfinance as yf

# como los informes de resultados de cada empresa son entregados los dias primero de enero de cada año
# lo que haremos sera especificar ese valor para cada principio de año:
# segun cada años serian: [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]
dolar_a_pesos = [6.79, 9.975, 13.75, 14.245, 16.67, 19.08, 39.5, 76, 163, 206.5, 345, 960]

# FORMATO                 [2022, 2021, 2020, 2019]
dolar_a_pesos = [ 345, 206.5, 163, 76]
dolar_a_pesos_2018 = 39.5

# ES DECIR QUE HAREMOS LAS CUENTAS A VALORES DEL DOLAR DE 2018      <-- IMPORTANTE
cuanto_seDevaluo_elDolar = [ 0.165, 0.079, 0.031, 0.018 ]

tiempo_actual = time.time()
estructura_tiempo = time.localtime(tiempo_actual)

anio_actual = estructura_tiempo.tm_year

def ajuste(i, valor):
    valor = valor/dolar_a_pesos[i]
    valor = valor - (valor*cuanto_seDevaluo_elDolar[i]) 
    return(valor)

def analisis(accion):
    if cedear == 'y':
        accion = accion+ '.BA'

    laAccion = yf.Ticker(accion)
    
        
    data = laAccion.info
    
    historial_precios = laAccion.history(period='max')

    IS = laAccion.income_stmt
    BS = laAccion.balance_sheet
    CF = laAccion.cashflow

    # Flujo de caja Libre
    cashflow = []
    for i in CF:
        FCF = CF[i]['Free Cash Flow']
        cashflow.append(FCF)
    cashflow.reverse()
    
    
    TotalAssets = []
    CurrentAssets = []
    TotalLiabilities = []
    CurrentLiabilities = []
    TotalEquity = []
    TotalDebt = []

    for i in BS:
        TA = BS[i]['Total Assets']
        TotalAssets.append(TA)
        CA = BS[i]['Current Assets']
        CurrentAssets.append(CA)
        TL = BS[i]['Total Liabilities Net Minority Interest']
        TotalLiabilities.append(TL)
        CL = BS[i]['Current Liabilities']
        CurrentLiabilities.append(CL)
        TE = BS[i]['Total Equity Gross Minority Interest']
        TotalEquity.append(TE)
        TD = BS[i]['Total Debt']
        TotalDebt.append(TD)
                

    NetIncome = []
    TotalIncome = []

    for i in IS:
        netCome = IS[i]['Net Income']
        totalCome = IS[i]['Total Revenue']
        NetIncome.append(netCome)
        TotalIncome.append(totalCome)




    # Aca ajustamos todos los valores al valor que tendrian en 2018
    if arg == "y":
        for i in range(4):
            TotalAssets[i] = ajuste(i,TotalAssets[i])
            CurrentAssets[i] = ajuste(i,CurrentAssets[i])
            TotalLiabilities[i] = ajuste(i,TotalLiabilities[i])
            CurrentLiabilities[i] = ajuste(i,CurrentLiabilities[i])
            NetIncome[i] = ajuste(i,NetIncome[i])
            TotalIncome[i] = ajuste(i,TotalIncome[i])
            TotalEquity[i] = ajuste(i,TotalEquity[i])
            TotalDebt[i] = ajuste(i,TotalDebt[i])
            cashflow[i] = ajuste(i,cashflow[i])
            
   



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

    ListaMargenIngTotales_IngNetos = []
    for i in range(4):
        MargenIngT_IngN = str(round((float(NetIncome[i]) / float(TotalIncome[i])) * 100)) + "%"
        ListaMargenIngTotales_IngNetos.append(MargenIngT_IngN)
    ListaMargenIngTotales_IngNetos.reverse()

    # Aca calulamos el ROA y el DtE promedio:
    promedioNetIncome = sum(NetIncome) / len(NetIncome)
    promedioActivos = sum(TotalAssets) / len(TotalAssets)
    promedioDebt = sum(TotalDebt) / len(TotalDebt)
    promedioEquity = sum(TotalEquity) / len(TotalEquity)

    Roa = promedioNetIncome / promedioActivos
    Dte = promedioDebt / promedioEquity
    # Aca vamos a calcular el Debt to Equity(deuda total / patrimonio total) y tambien vamos a calcular el roa(ingresos Netos / activos totales) en cada año:
    RoA = []
    DebtToEquity = []
    for i in range(4):
        roaa = NetIncome[i]/TotalAssets[i]
        RoA.append(roaa)
        DtE = TotalDebt[i]/TotalAssets[i]
        DebtToEquity.append(DtE)

    RoA.reverse()
    DebtToEquity.reverse()


    PEratio = data['trailingPE']
    EnterpriseValueToEBITDA = data['enterpriseToEbitda']
    PriceToSales = data['priceToSalesTrailing12Months']
    PriceToBook = data['priceToBook']

    print(f"{accion}:          los años en los que esta expresado este analisis son de la forma: [ {anio_actual-1}, {anio_actual-2}, {anio_actual-3}, {anio_actual-4} ]")
    print("----------------------------------")
    print("El historial del margen de ganancias (ingrNetos / ingrTotales) son: ",ListaMargenIngTotales_IngNetos)
    print("\n")
    print("El historial de Debt to Equity(deuda total / patrimonio total) es: ",DebtToEquity)
    print("\n")
    print("El historial de Return on Assets(ingresos Netos / activos totales) es: ",RoA)
    print("\n")
    print("El historial de Free cash flow(flujo de caja libre) es: ",cashflow)
    print("\n")
    print("lista del porcentaje de crecimiento de la diferencia NO corriente entre activos y pasivos: ",PorcentualTotalGrowthList)
    print("\n")
    print("lista del porcentaje de crecimiento de la diferencia corriente entre activos y pasivos: ",PorcentualCurrentGrowthList)
    print("\n")
    print("El Return on Assets promedio de la empresa es: ", Roa)
    print("\n")
    print("El Debt to Equity promedio de la empresa es: ", Dte)
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
    return(PEratio, EnterpriseValueToEBITDA, PriceToSales, PriceToBook, Roa, Dte)




print("AVISO: Hay ciertas acciones del mercado argentino(MERVAL) que necesiten que se ingrese un '.BA' (sin espacios) luego del simbolo por cuestiones de la API que estamos usando")
print("\n")
arg = input('¿La accion a analizar es argentina o es una cedear ubicado en estados unidos? si es afirmativa su respuesta excriba "y" (sin espacios ni comillas) y toque el ENTER. En caso negativo limitese a tocar el ENTER:  ')
cedear = input("¿la accion es un cedear argentino cotizando en estados unidos? (yes: 'y' + ENTER, no: ENTER):  ")
stock = input("Símbolo de la acción a analizar: ")
numCompe = int(input("con cuantas empresas de la misma industria desea comparar esta accion? (luego le preguntaremos cuales):  "))
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
    for j in range(6):
        compStock.append(datosDelStock[j])
    listaListas.append(compStock)
print(listaListas)

promedioPEratio = 0
promedioEnterpriseValueToEBITDA = 0
promedioPriceToSales = 0
promedioPriceToBook = 0
promedioRoa = 0
promedioDte = 0

for i in (listaListas):
    promedioPEratio += i[0]
    promedioEnterpriseValueToEBITDA += i[1]
    promedioPriceToSales += i[2]
    promedioPriceToBook += i[3]
    promedioRoa += i[4]
    promedioDte += i[5]

promedioPEratio/=(len(listaListas))
promedioEnterpriseValueToEBITDA/=(len(listaListas))
promedioPriceToSales/=(len(listaListas))
promedioPriceToBook/=(len(listaListas))
promedioRoa/=(len(listaListas))
promedioDte/=(len(listaListas))

print("el promedio de Price/Earnings ratio de la industria es: ",promedioPEratio)
print("el promedio de EnterpriseValue/EBITDA ratio de la industria es: ",promedioEnterpriseValueToEBITDA) 
print("el promedio de Price/Sales ratio de la industria es: ",promedioPriceToSales) 
print("el promedio de Price/Book ratio de la industria es: ",promedioPriceToBook)
print("el promedio de Return on Assets es: ",promedioRoa)  
print("el promedio de Debt to Equity es: ",promedioDte) 
print("\n")

print("\n")
print("recordemos que TTM significa que es un dato tomado de los ultimos 12 meses de la empresa")
print("\n")
print("El Price to Earnings(trailed): Un trailing P/E más alto puede indicar que el mercado tiene expectativas optimistas sobre el crecimiento futuro de las ganancias de la empresa, pero también podría indicar que la acción está sobrevalorada. Por otro lado, un trailing P/E más bajo podría sugerir que la acción podría estar infravalorada")
print("\n")
print("El Ev/Ebitda: Un bajo ratio EV/EBITDA puede indicar que la empresa está subvaluada en comparación con sus ganancias operativas. Sin embargo, es esencial considerar la industria y el ciclo de vida de la empresa al interpretar este ratio. Un ratio más bajo que el de la competencia podría sugerir que la empresa está relativamente infravalorada")
print("\n")
print("El Return on Assets evalúa la capacidad de una empresa para generar beneficios a partir de sus activos totales.")
print("\n")
print("El Debt to Equity mide la proporción de deuda en comparación con el capital propio de la empresa.")
print("\n")
print("El Price to Sales: Es especialmente útil para empresas que no generan beneficios o tienen beneficios volátiles. Un P/S bajo puede indicar que la empresa está infravalorada en relación con sus ingresos, pero se debe comparar con empresas similares en la industria.")
print("\n")
print("El Price to Book: Un P/B inferior a 1 podría indicar que la acción se está vendiendo por debajo de su valor contable, lo que podría considerarse una señal de que la acción está infravalorada \n ademas Un P/B superior a 1 indica que el mercado está dispuesto a pagar un precio mayor que el valor contable de la empresa. Esto podría deberse a expectativas positivas sobre el crecimiento futuro de la empresa, la calidad de sus activos, o la perspectiva de ganancias")
print("\n")
