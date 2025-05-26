<!-- templates/student.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>The Online Exam Proctor</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <header>
        <h1>The Online Exam Proctor</h1>
    </header>
    <main class="centered-card">
        <div class="exam-card">
            <h2>Exam Test</h2>
            <p>Answer the following questions within the time limit. Keep in mind that incorrect answers will penalize your score/time by 5 minutes!</p>
            <button onclick="startExam()">Start Quiz</button>
        </div>
    </main>
    <footer>
        <p>© The Online Exam Proctor System</p>
    </footer>

    <script>
        function startExam() {
            fetch("/start-exam")
                .then(res => res.json())
                .then(data => {
                    alert(Exam Completed!\nStatus: ${data.exam_status}\nTrust Score: ${data.trust_score});
                    window.location.href = "/admin";
                });
        }
    </script>
</body>
</html>
