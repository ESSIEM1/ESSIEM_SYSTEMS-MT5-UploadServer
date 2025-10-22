from flask import Flask, request, jsonify, render_template_string, make_response
import os
import subprocess
import time
import shutil

app = Flask(__name__)

# Generate a unique version ID for cache busting
VERSION_ID = str(int(time.time()))

UPLOAD_HTML = f'''
<!DOCTYPE html>
<html>
<head>
    <title>ESSIEM SYSTEMS MT5 Control Server</title>
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate, max-age=0">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
    <meta name="version" content="{VERSION_ID}">
    <style>
        body {{ font-family: Arial; margin: 40px; background: #1e1e1e; color: white; }}
        .container {{ max-width: 800px; margin: 0 auto; }}
        .header {{ text-align: center; margin-bottom: 30px; }}
        .brand {{ color: #007cba; font-size: 24px; font-weight: bold; }}
        .sub-brand {{ color: #00a8ff; font-size: 18px; }}
        .upload-area {{ 
            border: 2px dashed #007cba; 
            padding: 30px; 
            text-align: center;
            margin: 20px 0;
            border-radius: 8px;
            background: #2d2d2d;
        }}
        .btn {{ 
            background: #007cba; 
            color: white; 
            padding: 12px 25px; 
            border: none; 
            border-radius: 4px; 
            cursor: pointer;
            margin: 10px;
            font-size: 16px;
        }}
        .btn-danger {{ 
            background: #dc3545; 
            color: white; 
            padding: 12px 25px; 
            border: none; 
            border-radius: 4px; 
            cursor: pointer;
            margin: 10px;
            font-size: 16px;
        }}
        .btn-danger:hover {{
            background: #c82333;
        }}
        select, input[type="file"] {{ 
            padding: 10px; 
            margin: 10px; 
            border-radius: 4px;
            border: 1px solid #555;
            background: #333;
            color: white;
            width: 80%;
        }}
        .status {{ margin: 20px 0; padding: 15px; border-radius: 4px; text-align: center; }}
        .success {{ background: #2d5a2d; }}
        .error {{ background: #5a2d2d; }}
        .warning {{ background: #5a4d2d; }}
        .instructions {{ 
            margin-top: 30px; 
            padding: 20px; 
            background: #2d2d2d; 
            border-radius: 8px;
            border-left: 4px solid #007cba;
        }}
        .nuclear-section {{
            margin-top: 30px;
            padding: 20px;
            background: #3d2d2d;
            border-radius: 8px;
            border-left: 4px solid #dc3545;
            text-align: center;
        }}
        .confirm-box {{
            display: none;
            margin-top: 15px;
            padding: 15px;
            background: #5a2d2d;
            border-radius: 4px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="brand">ESSIEM SYSTEMS</div>
            <div class="sub-brand">- MT5 Control Server -</div>
            <div style="margin-top: 10px; font-size: 14px; color: #888;">
                essiemsystems.com - zbinvestmentgroup.com
            </div>
        </div>
        
        <p style="text-align: center; font-size: 16px;">
            Upload Expert Advisors, Indicators and Scripts directly to your MT5 terminal
        </p>
        
        <div class="upload-area" id="dropArea">
            <h3>📁 Upload File to MT5</h3>
            <form action="/upload?version={VERSION_ID}" method="post" enctype="multipart/form-data">
                <select name="file_type" required>
                    <option value="ea">Expert Advisor (.ex5)</option>
                    <option value="indicator">Indicator (.ex5)</option>
                    <option value="script">Script (.ex5)</option>
                </select><br>
                <input type="file" name="file" id="fileInput" accept=".ex5,.mq5" required>
                <br>
                <input type="submit" value="🚀 Upload to MT5" class="btn">
            </form>
        </div>
        
        <div id="status"></div>

        <div class="nuclear-section">
            <h3>⚠️ Nuclear Delete</h3>
            <p>Delete ALL personal data: MT5 logs, login credentials, server settings, and manually added Experts</p>
            <button class="btn-danger" onclick="showConfirm()">🧨 DELETE ALL PERSONAL FILES</button>
            
            <div id="confirmBox" class="confirm-box">
                <p><strong>⚠️ DANGER ZONE ⚠️</strong></p>
                <p>This will permanently delete:</p>
                <ul style="text-align: left; display: inline-block;">
                    <li>MT5 login credentials</li>
                    <li>Server settings</li>
                    <li>All log files</li>
                    <li>Manually added Experts/Indicators/Scripts</li>
                    <li>Chart settings and profiles</li>
                </ul>
                <p><strong>This action cannot be undone!</strong></p>
                <button class="btn-danger" onclick="nuclearDelete()">🔥 CONFIRM PERMANENT DELETE</button>
                <button class="btn" onclick="hideConfirm()" style="margin-left: 10px;">Cancel</button>
            </div>
        </div>
        
        <div class="instructions">
            <h3>📋 Instructions:</h3>
            <ol>
                <li><strong>Select file type</strong> (EA, Indicator, or Script)</li>
                <li><strong>Choose your .ex5 file</strong> from your computer</li>
                <li><strong>Click upload</strong> to transfer to MT5</li>
                <li><strong>Restart MT5</strong> MENU (File → Exit), Metatrader will restart automatically</li>
            </ol>
        </div>
    </div>
    
    <script>
        // Force cache clear
        window.onload = function() {{
            console.log('ESSIEM SYSTEMS MT5 Control Server - Version: {VERSION_ID}');
        }};
        
        document.getElementById('fileInput').onchange = function() {{
            if (this.files[0]) {{
                document.getElementById('status').innerHTML = 
                    '<div class="status">Ready to upload: <strong>' + this.files[0].name + '</strong></div>';
            }}
        }};
        
        // Add cache busting for form submission
        document.querySelector('form').addEventListener('submit', function() {{
            this.action = '/upload?version=' + Date.now();
        }});
        
        // Nuclear option functions
        function showConfirm() {{
            document.getElementById('confirmBox').style.display = 'block';
        }}
        
        function hideConfirm() {{
            document.getElementById('confirmBox').style.display = 'none';
        }}
        
        function nuclearDelete() {{
            if (confirm('FINAL WARNING: This will delete ALL personal data including login credentials. Are you absolutely sure?')) {{
                document.getElementById('status').innerHTML = '<div class="status warning">🧨 Deleting all personal files... This may take a moment.</div>';
                
                fetch('/nuclear_delete', {{ method: 'POST' }})
                    .then(response => response.json())
                    .then(data => {{
                        if (data.success) {{
                            document.getElementById('status').innerHTML = '<div class="status success">✅ ' + data.message + '</div>';
                        }} else {{
                            document.getElementById('status').innerHTML = '<div class="status error">❌ ' + data.message + '</div>';
                        }}
                        hideConfirm();
                    }})
                    .catch(error => {{
                        document.getElementById('status').innerHTML = '<div class="status error">❌ Error: ' + error + '</div>';
                        hideConfirm();
                    }});
            }}
        }}
    </script>
</body>
</html>
'''

@app.route('/')
def upload_page():
    response = make_response(render_template_string(UPLOAD_HTML))
    # Aggressive cache control headers
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.headers["Last-Modified"] = str(time.time())
    return response

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({"success": False, "message": "❌ No file selected"})
        
        file = request.files['file']
        file_type = request.form.get('file_type', 'ea')
        
        if file.filename == '':
            return jsonify({"success": False, "message": "❌ No file selected"})
        
        if not (file.filename.endswith('.ex5') or file.filename.endswith('.mq5')):
            return jsonify({"success": False, "message": "❌ Please upload .ex5 or .mq5 files only"})
        
        # Determine target directory
        if file_type == 'ea':
            target_dir = "Experts"
        elif file_type == 'indicator':
            target_dir = "Indicators" 
        else:  # script
            target_dir = "Scripts"
        
        # Save file to shared volume
        uploads_dir = "/uploads"
        os.makedirs(uploads_dir, exist_ok=True)
        temp_path = os.path.join(uploads_dir, file.filename)
        file.save(temp_path)
        
        # Check if MT5 container exists and is running
        check_container = subprocess.run([
            'docker', 'ps', '-q', '-f', 'name=essiem-mt5'
        ], capture_output=True, text=True)
        
        if not check_container.stdout.strip():
            os.remove(temp_path)
            return jsonify({
                "success": False, 
                "message": "❌ MT5 container is not running. Please start it first."
            })
        
        # CORRECT PATH: Portable MT5 installation at /home/mt5/program/
        mt5_base_path = "/home/mt5/program"
        final_mt5_path = f"{mt5_base_path}/MQL5/{target_dir}/{file.filename}"
        
        # First ensure the target directory exists
        mkdir_result = subprocess.run([
            'docker', 'exec', 'essiem-mt5', 'mkdir', '-p', f"{mt5_base_path}/MQL5/{target_dir}"
        ], capture_output=True, text=True)
        
        # Copy file to the portable MT5 directory
        copy_result = subprocess.run([
            'docker', 'cp', temp_path, f"essiem-mt5:{final_mt5_path}"
        ], capture_output=True, text=True)
        
        if copy_result.returncode != 0:
            os.remove(temp_path)
            return jsonify({
                "success": False, 
                "message": f"❌ Copy failed: {copy_result.stderr}"
            })
        
        # Fix permissions - VERY IMPORTANT for portable installation
        chown_result = subprocess.run([
            'docker', 'exec', 'essiem-mt5', 'chown', 'mt5:mt5', final_mt5_path
        ], capture_output=True, text=True)
        
        chmod_result = subprocess.run([
            'docker', 'exec', 'essiem-mt5', 'chmod', '755', final_mt5_path
        ], capture_output=True, text=True)
        
        # Verify file exists and has correct permissions
        verify_result = subprocess.run([
            'docker', 'exec', '-u', 'mt5', 'essiem-mt5', 'ls', '-la', final_mt5_path
        ], capture_output=True, text=True)
        
        # Clean up temp file
        os.remove(temp_path)
        
        if verify_result.returncode == 0:
            return jsonify({
                "success": True, 
                "message": f"✅ {file.filename} uploaded successfully to portable MT5 MQL5/{target_dir}/!\n\nPlease COMPLETELY CLOSE and RESTART MT5 to see it in Navigator.\n\nFile location: {final_mt5_path}"
            })
        else:
            return jsonify({
                "success": False, 
                "message": f"❌ Upload verification failed. File might be in wrong location."
            })
            
    except Exception as e:
        # Clean up temp file on error
        if 'temp_path' in locals() and os.path.exists(temp_path):
            os.remove(temp_path)
        return jsonify({"success": False, "message": f"❌ Upload failed: {str(e)}"})

@app.route('/nuclear_delete', methods=['POST'])
def nuclear_delete():
    """Delete all personal MT5 data: logs, credentials, settings, etc."""
    try:
        # Check if MT5 container is running
        check_container = subprocess.run([
            'docker', 'ps', '-q', '-f', 'name=essiem-mt5'
        ], capture_output=True, text=True)
        
        if not check_container.stdout.strip():
            return jsonify({
                "success": False, 
                "message": "❌ MT5 container is not running."
            })
        
        # List of directories/files to delete
        targets_to_delete = [
            # Logs
            "/home/mt5/program/logs",
            "/home/mt5/program/MQL5/Logs",
            # Config and profiles
            "/home/mt5/program/Config",
            "/home/mt5/program/Profiles", 
            "/home/mt5/program/MQL5/Profiles",
            # Tester results
            "/home/mt5/program/Tester",
            # Credentials and server settings (be careful with these)
            "/home/mt5/program/accounts.txt",
            "/home/mt5/program/*.srv",
            "/home/mt5/program/Config/*.srv",
        ]
        
        deleted_items = []
        
        for target in targets_to_delete:
            try:
                # Check if target exists
                check_result = subprocess.run([
                    'docker', 'exec', 'essiem-mt5', 'ls', target
                ], capture_output=True, text=True)
                
                if check_result.returncode == 0:
                    # Delete the target
                    delete_result = subprocess.run([
                        'docker', 'exec', 'essiem-mt5', 'rm', '-rf', target
                    ], capture_output=True, text=True)
                    
                    if delete_result.returncode == 0:
                        deleted_items.append(target.split('/')[-1])
            except:
                continue
        
        # Also delete any manually added Experts/Indicators/Scripts (but keep the directory structure)
        mql5_dirs = ["Experts", "Indicators", "Scripts"]
        for mql5_dir in mql5_dirs:
            try:
                # Delete contents but keep directory
                subprocess.run([
                    'docker', 'exec', 'essiem-mt5', 'find', f"/home/mt5/program/MQL5/{mql5_dir}", '-type', 'f', '-delete'
                ], capture_output=True)
                deleted_items.append(f"MQL5/{mql5_dir} files")
            except:
                continue
        
        # Recreate necessary directories
        subprocess.run([
            'docker', 'exec', 'essiem-mt5', 'mkdir', '-p', 
            '/home/mt5/program/Config',
            '/home/mt5/program/Profiles',
            '/home/mt5/program/Tester',
            '/home/mt5/program/logs',
            '/home/mt5/program/MQL5/Experts',
            '/home/mt5/program/MQL5/Indicators', 
            '/home/mt5/program/MQL5/Scripts',
            '/home/mt5/program/MQL5/Logs',
            '/home/mt5/program/MQL5/Profiles'
        ], capture_output=True)
        
        # Fix permissions
        subprocess.run([
            'docker', 'exec', 'essiem-mt5', 'chown', '-R', 'mt5:mt5', '/home/mt5/program/'
        ], capture_output=True)
        
        if deleted_items:
            return jsonify({
                "success": True,
                "message": f"✅ Nuclear delete completed! Deleted: {', '.join(deleted_items)}\n\nMT5 has been reset to factory state. All personal data removed."
            })
        else:
            return jsonify({
                "success": True,
                "message": "✅ No personal data found to delete. MT5 is already clean."
            })
            
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"❌ Nuclear delete failed: {str(e)}"
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
