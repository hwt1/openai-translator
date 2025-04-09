
import os
import sys
from flask import Flask, request, jsonify

from model.openai_model import OpenAIModel
from translator.pdf_translator import PDFTranslator

# 获取项目根路径的绝对路径
project_root =os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,project_root)

# 封装API方法
app = Flask(__name__)

# 定义API路由
@app.route('/translate',methods=['POST'])
def translate_api():
    # 获取请求中的 JSON数据
    data = request.get_json()

    model_name = data['model_name']
    pdf_file_path = data['pdf_file_path']

    model = OpenAIModel(model=model_name)
    # 实例化 PDFTranslator 类，并调用 translate_pdf() 方法
    translator = PDFTranslator(model)
    result = translator.translate_pdf(pdf_file_path)
    return jsonify({"result":result})

if __name__ == '__main__':
    app.run()