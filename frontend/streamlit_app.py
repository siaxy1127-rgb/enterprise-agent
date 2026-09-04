import requests
import streamlit as st

API_URL = "http://localhost:8000/chat"
REQUEST_TIMEOUT = 120

st.set_page_config(page_title="Enterprise Knowledge Agent")
st.title("Enterprise Knowledge Agent")

question = st.text_input("请输入问题")

if st.button("发送"):
    if not question or not question.strip():
        st.error("请输入问题后再发送。")
    else:
        try:
            response = requests.post(
                API_URL,
                json={"question": question.strip()},
                timeout=REQUEST_TIMEOUT,
            )
        except requests.exceptions.ConnectionError:
            st.error("无法连接 FastAPI 服务，请确认已启动：uvicorn app.main:app --reload")
        except requests.exceptions.Timeout:
            st.error("请求超时，请稍后重试。")
        except requests.exceptions.RequestException as exc:
            st.error(f"请求失败：{exc}")
        else:
            try:
                payload = response.json()
            except ValueError:
                st.error(f"接口返回了无法解析的响应（HTTP {response.status_code}）。")
            else:
                if not response.ok:
                    error_message = payload.get("error") or payload.get(
                        "detail",
                        f"接口调用失败（HTTP {response.status_code}）。",
                    )
                    st.error(error_message)
                else:
                    st.subheader("回答:")
                    st.write(payload.get("answer", ""))

                    st.subheader("引用来源:")
                    sources = payload.get("sources") or []
                    if not sources:
                        st.write("暂无引用来源")
                    else:
                        for source in sources:
                            st.markdown("来源文件:")
                            st.write(source.get("source", ""))
                            st.markdown("页码:")
                            st.write(source.get("page", ""))
                            st.markdown("内容:")
                            st.write(source.get("content", ""))
                            st.divider()
