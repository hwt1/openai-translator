
import os
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS

from model.openai_model import OpenAIModel
from translator.pdf_translator import PDFTranslator

# 获取项目根路径的绝对路径
project_root =os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,project_root)

# 封装API方法
app = Flask(__name__)

# 添加跨域处理
CORS(app)

# 定义API路由
# 测试请求
@app.route('/api/data',methods=['get'])
def test_data():
    result = "request success"
    return jsonify({"result":result})

@app.route('/translate',methods=['POST'])
def translate_api():
    # 获取请求中的 JSON数据
    data = request.get_json()

    model_name = data['model_name']
    pdf_file_path = data['pdf_file_path']

    model = OpenAIModel(model=model_name)
    # 实例化 PDFTranslator 类，并调用 translate_pdf() 方法
    translator = PDFTranslator(model)
    result = translator.translate_pdf(pdf_file_path=pdf_file_path)
    return jsonify({"result":result})

@app.route('/api/translate',methods=['POST'])
def translate_from_page():
    # 获取 modelName
    model_name = request.form.get('modelName')

    # 获取上传的文件
    file = request.files.get('file')
    if not file:
        return jsonify({'error':'文件未上传'}),400
    # 检查文件类型
    if file.filename.split('.')[-1].lower() !='pdf':
        return jsonify({'error':'只支持上传 PDF文件'}),400
    # 翻译后文件输出路径
    output_file_path = f"translated_files/{file.filename.replace(".pdf","_translated.pdf")}"

    model = OpenAIModel(model=model_name)
    # 实例化 PDFTranslator 类，并调用 translate_pdf() 方法
    translator = PDFTranslator(model)
    result = translator.translate_pdf(pdf_file=file,output_file_path=output_file_path)
    return jsonify({
        'status': 'success',
        'modelName': model_name,
        'fileName': file.filename,
        'result':result
    })
if __name__ == '__main__':
    app.run()