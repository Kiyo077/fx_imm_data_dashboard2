import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


#データフレームの読み込み
df_updown = pd.read_csv('df_immと日足終値_8週間後up or down_欠損値削除.csv',encoding='shift_jis',index_col=0)
df_updown.index = pd.to_datetime(df_updown.index)



#タイトル
st.header('■投機筋の売り買いポジションの差とレートの関係')

st.subheader('（1）IMMポジション')

# {通貨名}投機筋ポジションの列と{通貨ペア名}終値の列の選択(通貨列の削除)
col = [col for col in df_updown.columns if '通貨' not in col]
df_updown_imm_and_price = df_updown[col]


#通貨名をキーとして、各通貨IMMポジションと関連する通貨ペア列を選択
#「通貨」列に記載の各通貨名をデータフレームから選択（1行目のみ）
col_currency = [col for col in df_updown.columns if '通貨' in col]
list_currency = df_updown[col_currency].iloc[0].to_list()


#通貨を選択できるセレクトボックスを作成
currency_select = st.selectbox(
    '通貨',
    list_currency
)

#「終値」列の選択
col_price = [col for col in df_updown.columns if '終値' in col]

#通貨ペアを選択できるセレクトボックスを作成
currency_pair_select = st.selectbox(
    '通貨ペア',
    col_price
)



col_imm = [f'{currency_select}投機筋ロング',f'{currency_select}投機筋ショート',f'{currency_select}投機筋差']
col_price = [f'{currency_pair_select}']


df_updown_imm = df_updown[col_imm]
df_updown_price = df_updown[col_price]


#ラインチャートを作成
st.line_chart(df_updown_imm)



st.subheader('（2）IMMポジションとレートの関係（注意:「Autoscale」を押してください）')

#プロットの表示
fig = go.Figure()

#投機筋のポジションの差と終値をプロット
imm_data = df_updown_imm[f'{currency_select}投機筋差']

fig.add_trace(go.Scatter(x=df_updown_imm.index, y=df_updown_imm[f'{currency_select}投機筋差'],
                        mode='lines',
                        name=f'{currency_select}投機筋差'))

# 終値のプロット
fig.add_trace(go.Scatter(x=df_updown_price.index, y=df_updown_price[f'{currency_pair_select}'],
                    mode='lines',
                    name=f'{currency_pair_select}',
                    yaxis="y2"))


# y軸レイアウト
fig.update_layout(
    yaxis=dict(
        title="IMMポジション",  
        range=[-150000, 150000]  
    ),
    yaxis2=dict(
        title=f'{currency_pair_select}', 
        titlefont=dict(
            color="red"
        ),
        tickfont=dict(
            color="red"
        ),
        overlaying="y",
        side="right",
        range=[-200, 200]
    )
)


st.plotly_chart(fig)



#タイトル
st.title('■IMMポジションの分布と現在のIMMポジション')


#セレクトボックスで選択可能にするIMMポジションの列の選択
select_columns = [col for col in df_updown.columns if '通貨' not in col]
select_columns = [col for col in select_columns if '終値' not in col]
select_columns = [col for col in select_columns if '週間' not in col]
df_updown_select = df_updown[select_columns]
col_list = df_updown_select.columns


#セレクトボックスで選択可能にする通貨ペアのup or down列の選択
select_columns2 = [col for col in df_updown.columns if 'up or down' in col]
df_updown_select2 = df_updown[select_columns2]

col_list2 = df_updown_select2.columns


#セレクトボックスは（１）縦軸用、（２）横軸用、（３）up or down列用　3つ用意
option_imm1 = st.selectbox(
    'X軸:投機筋ポジション',
    (col_list))

option_imm2 = st.selectbox(
    'y軸:投機筋ポジション2',
    (col_list))

option_imm3 = st.selectbox(
    '通貨ペアup or down',
    (col_list2))


#列の要素がupおよびdownだと、プロットを色分けしてくれなかったので、カラーコードに置き換え
color_dict = {'up': '#FFC0CB', 'down': '#87CEFA'}  
colors = df_updown[option_imm3].map(color_dict)


#updown列のupのみを表示。凡例をupとdownでそれぞれ変えたい
scatter1 = go.Scatter(
    x=df_updown[option_imm1][colors == '#FFC0CB'],
    y=df_updown[option_imm2][colors == '#FFC0CB'],
    mode='markers',
    marker=dict(color=colors[colors == '#FFC0CB']),
    name='8週間後up'
)


#updown列のdownのみを表示。
scatter2 = go.Scatter(
    x=df_updown[option_imm1][colors == '#87CEFA'],
    y=df_updown[option_imm2][colors == '#87CEFA'],
    mode='markers',
    marker=dict(color=colors[colors == '#87CEFA']),
    name='8週間後down'
)


#x軸、y軸名を設定
layout = go.Layout(
    xaxis=dict(title=option_imm1),
    yaxis=dict(title=option_imm2),
)


#最新日のポジションの行を抽出
df_updown_0 = pd.DataFrame(df_updown.iloc[0]).T


#最新日のIMMポジションをプロット
plot = go.Scatter(
    x=df_updown_0[option_imm1],
    y=df_updown_0[option_imm2],
    mode = 'markers',
    marker=dict(
        color='red',
        symbol='star',
        size=15),
    name='現在のIMMポジション'
    )


#散布図とプロットを同じグラフに表示させたいので
fig = go.Figure(data=[scatter1,scatter2, plot], layout=layout)
st.plotly_chart(fig)



#タイトル
st.header('※最新日の各通貨のIMMポジション')


#通貨を選択できるセレクトボックス 同じ名前の通貨選択セレクトボックスを上で作成しているので「2」をつけています
col_country = [col for col in df_updown.columns if '通貨' in col]
list_country = df_updown[col_country].iloc[0].to_list()

option_country = st.selectbox(
    '通貨選択',
    (list_country)
)


#データフレームのうち、{通貨名}投機筋ロングから{通貨名}投機筋差までの3列を選択し、バーチャートにする
df_updown_imm_only = df_updown.loc[:,'USD投機筋ロング':'NZD投機筋差']
df_updown_imm_only_select = df_updown_imm_only.loc[:,f'{option_country}投機筋ロング':f'{option_country}投機筋差']
df_updown_imm_only_select_new = pd.DataFrame(df_updown_imm_only_select.iloc[0,:]).T.values[0]

x_list = [f'{option_country}投機筋ロング',f'{option_country}投機筋ショート',f'{option_country}投機筋差']

fig = px.bar(
    df_updown_imm_only_select_new,
    x=df_updown_imm_only_select_new,
    y=x_list,
    color=df_updown_imm_only_select_new,
    width=600,
    height=300)


st.plotly_chart(fig)


#　※plotlyのanimation_frameを使ってみたかっただけ

x_list2 = ['USD投機筋ロング','USD投機筋ショート','USD投機筋差','EUR投機筋ロング','EUR投機筋ショート','EUR投機筋差',
'JPY投機筋ロング','JPY投機筋ショート','JPY投機筋差','GBP投機筋ロング','GBP投機筋ショート','GBP投機筋差',
'AUD投機筋ロング','AUD投機筋ショート','AUD投機筋差','CHF投機筋ロング','CHF投機筋ショート','CHF投機筋差',
'CAD投機筋ロング','CAD投機筋ショート','CAD投機筋差','NZD投機筋ロング','NZD投機筋ショート','NZD投機筋差']

df_updown_imm_only2 = df_updown[x_list2]
df_updown_imm_only_select_new2 = pd.DataFrame(df_updown_imm_only2.iloc[0,:]).T.values[0]


fig2 = px.bar(
    df_updown_imm_only_select_new2,
    x=x_list2,
    y=df_updown_imm_only_select_new2,
    color=df_updown_imm_only_select_new2,
    animation_frame=x_list2,
    range_y=[-150000,150000],
    width=400,
    height=600)



st.plotly_chart(fig2)



st.text('出典:Commodity Futures Trading Commission | CFTC')
st.text('出典:AXIORY')
st.text('出典:セントラル短資fx')
st.text('本結果は、（1）IMMデータ:Commodity Futures Trading Commission | CFTC、（2）日足終値:AXIORYおよびセントラル短資fx、からダウンロードしたデータを加工してグラフを作成しています。')
