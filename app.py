import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Affiliate Helper", page_icon="🛍️", layout="centered")

st.title("🛍️ Affiliate Link & Caption Generator")
st.caption("ระบบช่วยแปลงลิงก์และเขียนแคปชันสำหรับ TikTok / Shopee บนมือถือ")

original_url = st.text_input("🔗 วางลิงก์สินค้า (Shopee/TikTok Shop):", placeholder="https://...")
tone = st.selectbox(
    "🎨 เลือกสไตล์แคปชัน:", 
    ["สายป้ายยาปั่นๆ", "เน้นสเปก/รีวิวความรู้สึก", "สั้นกระชับเน้นโปรโมชัน", "เน้นจุดเด่นแก้ปัญหา"]
)
user_api_key = st.text_input("🔑 ใส่ Gemini API Key ของคุณ:", type="password")

if st.button("⚡ สร้างแคปชันและเตรียมลิงก์", use_container_width=True):
    if not original_url:
        st.warning("⚠️ กรุณากรอกลิงก์สินค้าด้วยครับ")
    elif not user_api_key:
        st.warning("⚠️ กรุณากรอก Gemini API Key ด้วยครับ")
    else:
        with st.spinner("⏳ กำลังสร้างแคปชัน..."):
            try:
                genai.configure(api_key=user_api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"""
                ช่วยเขียนแคปชันขายของภาษาไทยสั้นๆ ปังๆ สำหรับอัปโพสต์ลง TikTok Video หรือ Shopee Video 
                รายละเอียด:
                - สไตล์ข้อความ: {tone}
                - ลิงก์/ข้อมูลสินค้า: {original_url}
                - ใส่ Emoji ให้น่าอ่าน มีแฮชแท็กยอดฮิต 3-5 อัน
                - ใส่ข้อความเชิญชวนให้คนกดปักตะกร้า หรือจิ้มลิงก์
                """
                
                response = model.generate_content(prompt)
                generated_caption = response.text
                
                st.success("✅ สร้างเรียบร้อย!")
                st.subheader("📝 แคปชันที่ได้ (กดก๊อปปี้ได้เลย):")
                st.code(generated_caption, language=None)
                
                st.subheader("🔗 ลิงก์สินค้า:")
                st.code(original_url, language=None)
                
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาด: {e}")
