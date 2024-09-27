import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

df = pd.read_csv('fcc-forum-pageviews.csv', index_col='date', parse_dates=True)

# Remove dados fora do range de 2.5% a 97.5%
df = df[
    (df['value'] >= df['value'].quantile(0.025)) &
    (df['value'] <= df['value'].quantile(0.975))
]


def draw_line_plot():
    # Configurações do plot
    fig, ax = plt.subplots(figsize=(20, 5))
    ax.plot(df['value'])
    
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")
    
    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    # Modifica o dataframe para agrupar dados de ano e mês
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month_name()

    # Calcula a média e separa os valores dos grupos em colunas
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    fig = df_bar.plot(kind='bar', figsize=(12, 6), legend=True).figure
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')

    plt.legend(title='Months', labels=[
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ], bbox_to_anchor=(1.05, 1), loc='upper left')

    # Ajusta o layout para evitar que as barras sejam cortadas
    plt.tight_layout()

    fig.savefig('bar_plot.png')
    return fig


def draw_box_plot():
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    fig, axs = plt.subplots(1, 2, figsize=(10, 7))
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    # Garante a categorização da coluna mês na ordem estabelecida
    df_box['month'] = pd.Categorical(df_box['month'], categories=months, ordered=True)
    
    sns.boxplot(x=df_box['year'], y=df_box['value'], ax=axs[0])
    axs[0].set_title('Year-wise Box Plot (Trend)')
    axs[0].set_xlabel('Year')
    axs[0].set_ylabel('Page Views')

    sns.boxplot(x=df_box['month'], y=df_box['value'], ax=axs[1])
    axs[1].set_title('Month-wise Box Plot (Seasonality)')
    axs[1].set_xlabel('Month')
    axs[1].set_ylabel('Page Views')

    fig.savefig('box_plot.png')
    return fig