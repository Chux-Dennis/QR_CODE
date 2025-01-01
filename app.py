from flask import Flask, request, jsonify, send_file
import qrcode
import io

app = Flask(__name__)

@app.route('/get-code', methods=['POST'])
def generate_qr_code():
    try:
        # Parse JSON body
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({"error": "Invalid request. Please provide a 'url' property."}), 400
        
        url = data['url']
        if not isinstance(url, str) or not url.strip():
            return jsonify({"error": "Invalid 'url'. It must be a non-empty string."}), 400
        
        # Generate QR Code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        # Create an image
        img = qr.make_image(fill_color="black", back_color="white")

        # Convert image to bytes
        img_io = io.BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)

        # Return the image as a response
        return send_file(img_io, mimetype='image/png')

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)

