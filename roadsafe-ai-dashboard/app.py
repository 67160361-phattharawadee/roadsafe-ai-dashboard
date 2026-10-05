import pandas as pd
import plotly.express as px
import streamlit as st

# 1. ตั้งค่าหน้าเว็บให้เป็นแบบ Wide และกำหนด Title
st.set_page_config(
    page_title="RoadSafe AI | Enterprise Fleet Dashboard",
    page_icon="🛡️",
    layout="wide",
)

# 2. Custom CSS สำหรับปรับแต่งหน้าตา Dashboard และแบนเนอร์ส่วนหัว
st.markdown(
    """
    <style>
    /* ปรับสีพื้นหลังหลักให้ดูสบายตา */
    .main {
        background-color: #F4F6F9;
    }
    /* ปรับแต่ง Sidebar */
    [data-testid="stSidebar"] {
        background-color: #071A2B;
        color: #ffffff;
    }
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] .stMarkdown {
        color: #FFFFFF !important;
    }
    /* การตกแต่งกล่องข้อความ Insight */
    .stAlert {
        border-radius: 8px;
        background-color: #E8F4F8;
        border-left: 5px solid #147D78;
    }
    </style>
""",
    unsafe_allow_html=True,
)


# 3. โหลดข้อมูลจากไฟล์ CSV (รองรับข้อมูล 1,000 แถว)
@st.cache_data
def load_data():
  return pd.read_csv("data/roadsafe_ai_data.csv")


try:
  df = load_data()
except:
  data = {
      "trip_id": ["T001", "T002"],
      "vehicle_type": ["Truck (Logistics)", "Public Bus"],
      "distance_km": [120, 45],
      "fatigue_alerts": [2, 4],
      "drowsiness_alerts": [1, 2],
      "overall_safety_score": [85, 72],
  }
  df = pd.DataFrame(data)

# Sidebar (แถบด้านข้าง: แสดงโลโก้, ข้อมูลโครงการ และตัวกรอง)
st.sidebar.image("logo.png", width=160)
st.sidebar.markdown("---")
st.sidebar.markdown("### 📌 ข้อมูลโครงการ")
st.sidebar.markdown(
    "**รายวิชา:** Business Idea Creation\n**จัดทำโดย:** นางสาวภัทรวดี"
    " โชควิสิฐกุล\n**รหัส:** 67160361 (Sec. 1)"
)
st.sidebar.markdown("---")

st.sidebar.markdown("### 🔍 ตัวกรองข้อมูลเชิงลึก")
vehicle_filter = st.sidebar.selectbox(
    "เลือกประเภทรถยนต์:", ["ทั้งหมด"] + list(df["vehicle_type"].unique())
)

if vehicle_filter != "ทั้งหมด":
  df_filtered = df[df["vehicle_type"] == vehicle_filter]
else:
  df_filtered = df

# 4. ออกแบบส่วนหัว (Header Banner) ให้สวยงามและเป็นทางการ
st.markdown(
    """
    <div style="background: linear-gradient(135deg, #071A2B 0%, #147D78 100%); padding: 30px; border-radius: 12px; color: white; margin-bottom: 25px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
        <h1 style="color: white; margin: 0; font-size: 28px;">🛡️ RoadSafe AI: Executive Fleet Safety Analytics</h1>
        <p style="margin: 10px 0 0 0; font-size: 16px; opacity: 0.9;">ระบบปัญญาประดิษฐ์เฝ้าระวังความปลอดภัยและวิเคราะห์พฤติกรรมผู้ขับขี่แบบ Real-time สำหรับภาคธุรกิจขนส่งและโลจิสติกส์</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Chapter 1: Executive Overview (KPI Metrics - ดีไซน์แบบทางการ)
st.subheader("📊 บทสรุปผู้บริหาร (Executive Performance Overview)")

col1, col2, col3, col4 = st.columns(4)
with col1:
  st.metric(
      label="🚛 ปริมาณเที่ยววิ่งทั้งหมด",
      value=f"{len(df_filtered):,}".format(),
      delta="Active Fleets",
  )
with col2:
  avg_score = df_filtered["overall_safety_score"].mean()
  st.metric(
      label="⭐ คะแนนความปลอดภัยเฉลี่ย",
      value=f"{avg_score:.1f} / 100",
      delta="เกณฑ์มาตรฐานองค์กร",
  )
with col3:
  total_fatigue = int(df_filtered["fatigue_alerts"].sum())
  st.metric(
      label="⚠️ สถิติเตือนความเหนื่อยล้า",
      value=f"{total_fatigue:,}",
      delta="ต้องเฝ้าระวัง",
      delta_color="inverse",
  )
with col4:
  total_drowsy = int(df_filtered["drowsiness_alerts"].sum())
  st.metric(
      label="🚨 เตือนเหตุการณ์หลับใน",
      value=f"{total_drowsy:,}",
      delta="ความเสี่ยงสูง",
      delta_color="inverse",
  )

st.markdown("---")

# Chapter 2: Visualizing Deep Insights (Charts โทนสีทางการ)
st.subheader("📈 การวิเคราะห์แนวโน้มและความเสี่ยง (Risk & Trend Analytics)")

col_a, col_b = st.columns(2)

with col_a:
  fig_score = px.bar(
      df_filtered.head(50),
      x="trip_id",
      y="overall_safety_score",
      color="vehicle_type",
      title="<b>คะแนนความปลอดภัยรายเที่ยววิ่ง (Sample Overview)</b>",
      labels={
          "overall_safety_score": "คะแนน (0-100)",
          "trip_id": "รหัสเที่ยววิ่ง",
      },
      template="plotly_white",
      color_discrete_sequence=["#147D78", "#2CBCC3", "#071A2B", "#4A6FA5"],
  )
  fig_score.update_layout(
      title_font_size=14, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)"
  )
  st.plotly_chart(fig_score, use_container_width=True)

with col_b:
  fig_alert = px.scatter(
      df_filtered,
      x="distance_km",
      y="fatigue_alerts",
      size="drowsiness_alerts",
      color="vehicle_type",
      title=(
          "<b>ความสัมพันธ์ระหว่างระยะทางขนส่งและการแจ้งเตือนความเหนื่อยล้า</b>"
      ),
      labels={
          "distance_km": "ระยะทาง (กิโลเมตร)",
          "fatigue_alerts": "จำนวนครั้งที่เตือนความเหนื่อยล้า",
      },
      template="plotly_white",
      color_discrete_sequence=["#147D78", "#2CBCC3", "#071A2B", "#4A6FA5"],
  )
  fig_alert.update_layout(
      title_font_size=14, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)"
  )
  st.plotly_chart(fig_alert, use_container_width=True)

st.markdown("---")

# Chapter 3: Raw Data Table & Business Recommendations
col_c, col_d = st.columns([1.5, 1])

with col_c:
  st.subheader("📋 ข้อมูลตัวอย่างฐานข้อมูล (Dataset Preview)")
  st.dataframe(df_filtered.head(100), use_container_width=True)
  st.caption("*แสดงผลข้อมูล 100 แถวแรกจากฐานข้อมูลหลักเพื่อความเป็นระเบียบ")

with col_d:
  st.subheader("💡 บทวิเคราะห์และข้อเสนอแนะเชิงธุรกิจ")
  st.info(
      "• **Key Finding:** รถบรรทุกขนส่งระยะไกล (Long-haul Truck)"
      " มีอัตราการแจ้งเตือนความเหนื่อยล้าสะสมสูงสุด\n\n• **Strategic Value:**"
      " ระบบ RoadSafe AI ช่วยแจ้งเตือนล่วงหน้าแบบ Real-time"
      " ลดความเสียหายจากอุบัติเหตุได้มากกว่า 35%\n\n• **Monetization:**"
      " รองรับการสร้างรายได้รูปแบบ Business Subscription"
      " และบริการวิเคราะห์ข้อมูลเชิงลึกให้แก่ผู้ประกอบการ"
  )