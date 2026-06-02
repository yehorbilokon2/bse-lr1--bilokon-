import os
from flask import Flask, jsonify, request
from document_manager import DocumentManager

app = Flask(__name__)
manager = DocumentManager()

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"}), 200

@app.route('/api/analyze', methods=['POST'])
def analyze_document():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Відсутні дані у форматі JSON"}), 400
        
    file_name = data.get("file_name")
    size_mb = data.get("size_mb")
    
    if file_name is None or size_mb is None:
        return jsonify({"error": "Поля 'file_name' та 'size_mb' є обов'язковими"}), 400
        
    try:
        doc = manager.upload_document(file_name, float(size_mb))

        analysis_result = manager.analyze(doc)
        
        return jsonify({
            "message": "Документ успішно завантажено та проаналізовано",
            "document": {
                "id": doc.id,
                "file_name": doc.file_name,
                "size_mb": doc.size_mb,
                "tags": doc.tags
            },
            "analysis": analysis_result
        }), 200
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Внутрішня помилка сервера", "details": str(e)}), 500

if __name__ == '__main__':

    host = "0.0.0.0" if os.environ.get("RENDER") else "127.0.0.1"
    
    port = int(os.environ.get("PORT", 5000))
    
    print(f"Запуск сервера на http://{host}:{port}")
    app.run(host=host, port=port)