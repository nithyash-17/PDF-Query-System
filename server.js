const express = require('express');
const path = require('path');
const multer = require('multer');
const { spawn } = require('child_process');
const fs = require('fs');
const cors = require('cors');

const app = express();
app.use(cors());

const port = 3000;

// Serve static files (frontend) from the 'public' folder
app.use(express.static(path.join(__dirname, 'public')));

// Parse JSON bodies for our API endpoints
app.use(express.json());

// Configure multer to store uploaded PDFs in the 'pdfs' folder using their original names
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, path.join(__dirname, 'pdfs'));
  },
  filename: function (req, file, cb) {
    cb(null, file.originalname);
  }
});
const upload = multer({ storage });

// Helper function to run a Python script
function runPythonScript(scriptName, args, callback) {
  const scriptPath = path.join(__dirname, 'python-scripts', scriptName);
  const pythonProcess = spawn('python', [scriptPath, ...args], { cwd: path.join(__dirname, 'python-scripts') });

  let stdoutData = '';
  let stderrData = '';

  pythonProcess.stdout.on('data', (data) => {
    stdoutData += data.toString();
  });

  pythonProcess.stderr.on('data', (data) => {
    stderrData += data.toString();
  });

  pythonProcess.on('close', (code) => {
    if (code !== 0) {
      return callback(new Error(`Script ${scriptName} exited with code ${code}. Stderr: ${stderrData}`));
    }
    const results = stdoutData.split('\n').filter(line => line.trim() !== '');
    callback(null, results);
  });
}

// ------------------------------
// Endpoint: PDF Ingestion & Processing (triggered by upload)
// ------------------------------
app.post('/upload', upload.array('pdfs', 10), (req, res) => {
  console.log('Received PDF files:', req.files);

  runPythonScript('pdf_to_text.py', [], (err) => {
    if (err) {
      console.error('Error in pdf_to_text.py:', err);
      return res.status(500).json({ error: err.toString() });
    }
    console.log('PDF extraction complete.');

    runPythonScript('preprocess_text.py', [], (err2) => {
      if (err2) {
        console.error('Error in preprocess_text.py:', err2);
        return res.status(500).json({ error: err2.toString() });
      }
      console.log('Text preprocessing complete.');

      runPythonScript('create_embeddings.py', [], (err3) => {
        if (err3) {
          console.error('Error in create_embeddings.py:', err3);
          return res.status(500).json({ error: err3.toString() });
        }
        console.log('Embedding creation complete.');

        // Final response to the frontend
        res.json({
          message: 'File processed, you may now ask queries.'
        });
      });
    });
  });
});

// ------------------------------
// Endpoint: Query Processing & Answer Generation
// ------------------------------
app.post('/query', (req, res) => {
  const question = req.body.question;
  if (!question) {
    return res.status(400).json({ error: 'Question is required.' });
  }

  const indexPath = path.join(__dirname, 'python-scripts/faiss_index.index');

  fs.access(indexPath, fs.constants.F_OK, (err) => {
    if (err) {
      console.log('FAISS index not found. Running ingestion pipeline before processing query...');
      runPythonScript('pdf_to_text.py', [], (err) => {
        if (err) return res.status(500).json({ error: err.toString() });
        console.log('PDF extraction complete.');

        runPythonScript('preprocess_text.py', [], (err2) => {
          if (err2) return res.status(500).json({ error: err2.toString() });
          console.log('Text preprocessing complete.');

          runPythonScript('create_embeddings.py', [], (err3) => {
            if (err3) return res.status(500).json({ error: err3.toString() });
            console.log('Embedding creation complete.');

            processQuery(question, res);
          });
        });
      });
    } else {
      processQuery(question, res);
    }
  });
});

function processQuery(question, res) {
  runPythonScript('query_engine.py', [question], (err, queryResults) => {
    if (err) {
      console.error('Error in query_engine.py:', err);
      return res.status(500).json({ error: err.toString() });
    }

    console.log('Raw query engine output:', queryResults);
    const lastLine = queryResults.filter(line => line.trim().startsWith('{')).pop();

    let resultObj;
    try {
      resultObj = JSON.parse(lastLine);
    } catch (e) {
      console.error('Failed to parse query engine output as JSON:', e, "Raw output:", queryResults);
      return res.status(500).json({ error: 'Invalid JSON response from query engine.' });
    }

    res.json(resultObj);
  });
}

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
