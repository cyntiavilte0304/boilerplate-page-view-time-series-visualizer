import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# 1. Importar datos y establecer la fecha como índice
# Se carga el CSV y la columna 'date' se convierte en índice de tipo datetime.
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# 2. Limpiar datos (filtrar top 2.5% y bottom 2.5%)
# Se descartan valores extremos para mejorar la calidad del análisis.
df = df[
    (df['value'] >= df['value'].quantile(0.025)) &
    (df['value'] <= df['value'].quantile(0.975))
]


# 3. Gráfico de líneas
def draw_line_plot():
    # Se crea una copia para no modificar el DataFrame original.
    df_line = df.copy()

    # Crear figura
    fig, ax = plt.subplots(figsize=(15, 5))

    # Dibujar línea
    ax.plot(df_line.index, df_line['value'], color='red')

    # Título y etiquetas
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    # Guardar imagen
    fig.savefig('line_plot.png')
    return fig


# 4. Gráfico de barras (promedio mensual por año)
def draw_bar_plot():
    # Se crea copia y se agregan columnas para año y mes.
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month_name()

    # Agrupar por año y mes
    df_grouped = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    # Crear figura
    fig = df_grouped.plot(kind='bar', figsize=(12, 8)).figure

    # Títulos y etiquetas
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(title='Months')

    # Guardar imagen
    fig.savefig('bar_plot.png')
    return fig


# 5. Diagramas de caja (año y mes)
def draw_box_plot():
    # Se prepara la data reiniciando el índice y extrayendo año/mes.
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = df_box['date'].dt.year
    df_box['month'] = df_box['date'].dt.strftime('%b')

    # Orden correcto de meses
    month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    # Crear figura
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    # Boxplot por año
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')

    # Boxplot por mes
    sns.boxplot(x='month', y='value', data=df_box,
                order=month_order, ax=axes[1])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    # Guardar imagen
    fig.savefig('box_plot.png')
    return fig
