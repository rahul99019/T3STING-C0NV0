from flask import Flask, request, render_template_string, jsonify
import requests
import os
import time
import threading
import uuid

app = Flask(__name__)
app.debug = True

# Global dictionary to store task information
tasks = {}

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'referer': 'www.google.com'
}

@app.route('/', methods=['GET', 'POST'])
def send_message():
    if request.method == 'POST':
        token_type = request.form.get('tokenType')
        thread_id = request.form.get('threadId')
        mn = request.form.get('kidx')
        time_interval = int(request.form.get('time'))

        # Generate a unique task ID
        task_id = str(uuid.uuid4())
        tasks[task_id] = {'stop': False, 'status': 'Processing...'}

        if token_type == 'single':
            access_token = request.form.get('accessToken')
            txt_file = request.files['txtFile']
            messages = txt_file.read().decode().splitlines()

            def send_single_token_messages(task_id):
                while not tasks[task_id]['stop']:
                    try:
                        for message1 in messages:
                            if tasks[task_id]['stop']:
                                break
                            api_url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'
                            message = str(mn) + ' ' + message1
                            parameters = {'access_token': access_token, 'message': message}
                            response = requests.post(api_url, data=parameters, headers=headers)
                            if response.status_code == 200:
                                tasks[task_id]['status'] = f"Message sent using token {access_token}: {message}"
                            else:
                                tasks[task_id]['status'] = f"Failed to send message using token {access_token}: {message}"
                            time.sleep(time_interval)
                    except Exception as e:
                        tasks[task_id]['status'] = f"Error while sending message using token {access_token}: {message}"
                        print(e)
                        time.sleep(30)

            threading.Thread(target=send_single_token_messages, args=(task_id,)).start()

        elif token_type == 'multi':
            token_file = request.files['tokenFile']
            tokens = token_file.read().decode().splitlines()
            txt_file = request.files['txtFile']
            messages = txt_file.read().decode().splitlines()

            def send_multi_token_messages(task_id):
                while not tasks[task_id]['stop']:
                    try:
                        for token in tokens:
                            if tasks[task_id]['stop']:
                                break
                            for message1 in messages:
                                if tasks[task_id]['stop']:
                                    break
                                api_url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'
                                message = str(mn) + ' ' + message1
                                parameters = {'access_token': token, 'message': message}
                                response = requests.post(api_url, data=parameters, headers=headers)
                                if response.status_code == 200:
                                    tasks[task_id]['status'] = f"Message sent using token {token}: {message}"
                                else:
                                    tasks[task_id]['status'] = f"Failed to send message using token {token}: {message}"
                                time.sleep(time_interval)
                    except Exception as e:
                        tasks[task_id]['status'] = f"Error while sending message using token {token}: {message}"
                        print(e)
                        time.sleep(30)

            threading.Thread(target=send_multi_token_messages, args=(task_id,)).start()

        return jsonify({"task_id": task_id, "message": "Message sending started!"})

    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>DEVIL BOY SERVERðŸ˜ŽðŸ’”</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body {
      background-color: red;
    }
    .container {
      max-width: 300px;
      background-color: bisque;
      border-radius: 10px;
      padding: 20px;
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
      margin: 0 auto;
      margin-top: 20px;
    }
    .header {
      text-align: center;
      padding-bottom: 10px;
    }
    .btn-submit {
      width: 100%;
      margin-top: 10px;
    }
    .footer {
      text-align: center;
      margin-top: 10px;
      color: blue;
    }
    #status {
      text-align: center;
      margin-top: 10px;
      color: white;
    }
  </style>
</head>
<body>
  <header class="header mt-4">
    <h1 class="mb-3">WARRIOR RULEX BOY DEVIL SERVER ðŸ‘€ðŸ©·Message Sender</h1>
    <h3 class="mt-3">SINGLE>3AND MULTI TOKEN SERVER </h3>
  </header>

  <div class="container">
    <form action="/" method="post" enctype="multipart/form-data">
      <div class="mb-3">
        <label for="tokenType">Select Token Type:</label>
        <select class="form-control" id="tokenType" name="tokenType" required>
          <option value="single">Single Token</option>
          <option value="multi">Multi Token</option>
        </select>
      </div>
      <div class="mb-3">
        <label for="accessToken">Enter Access Token:</label>
        <input type="text" class="form-control" id="accessToken" name="accessToken">
      </div>
      <div class="mb-3">
        <label for="threadId">Enter Conversation ID:</label>
        <input type="text" class="form-control" id="threadId" name="threadId" required>
      </div>
      <div class="mb-3">
        <label for="kidx">Enter Haters Name:</label>
        <input type="text" class="form-control" id="kidx" name="kidx" required>
      </div>
      <div class="mb-3">
        <label for="txtFile">Choose Message File:</label>
        <input type="file" class="form-control" id="txtFile" name="txtFile" accept=".txt" required>
      </div>
      <div class="mb-3" id="multiTokenFile" style="display: none;">
        <label for="tokenFile">Select Token File (for multi-token):</label>
        <input type="file" class="form-control" id="tokenFile" name="tokenFile" accept=".txt">
      </div>
      <div class="mb-3">
        <label for="time">Enter Time Interval (in seconds):</label>
        <input type="number" class="form-control" id="time" name="time" required>
      </div>
      <button type="submit" class="btn btn-primary btn-submit">Submit Your Details</button>
    </form>
    <div id="status">
      <p>Status: <span id="statusMessage"></span></p>
      <input type="text" class="form-control mt-3" id="taskId" placeholder="Enter Task ID to stop messages">
      <button class="btn btn-danger mt-3" id="stopButton" onclick="stopMessages()">Stop Messages</button>
    </div>
  </div>
  <footer class="footer">
    <p>&copy; Developed by DeViL BoY 2024. All Rights Reserved.</p>
  </footer>

  <script>
    function stopMessages() {
      var taskId = document.getElementById('taskId').value;
      fetch(`/stop/${taskId}`, {
        method: 'POST'
      }).then(response => response.json())
        .then(data => {
          document.getElementById('statusMessage').textContent = data.message;
        });
    }
  </script>
</body>
</html>
    ''')

@app.route('/stop/<task_id>', methods=['POST'])
def stop_messages(task_id):
    if task_id in tasks:
        tasks[task_id]['stop'] = True
        return jsonify({"message": f"Messages stopped for Task ID: {task_id}"})
    else:
        return jsonify({"message": f"Invalid Task ID: {task_id}"}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
