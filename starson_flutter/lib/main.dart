
import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:firebase_core/firebase_core.dart';
// import 'package:firebase_vertexai/firebase_vertexai.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp();
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'StarSon POS',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const MyHomePage(title: 'StarSon POS Home'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  String? _analysisResult;
  bool _isLoading = false;

  Future<void> _analyzeInventoryImage() async {
    setState(() {
      _isLoading = true;
      _analysisResult = null;
    });

    final picker = ImagePicker();
    final XFile? imageFile = await picker.pickImage(source: ImageSource.gallery);

    if (imageFile == null) {
      setState(() {
        _isLoading = false;
      });
      return;
    }

    try {
      // final model = FirebaseVertexAI.instance.geminiProVision();
      // final prompt = TextPart("Analyze this image of a store's inventory. Return a JSON object where keys are the item names and values are their quantities. For example: {'item_name': quantity}");
      // final imageBytes = await imageFile.readAsBytes();
      // final imagePart = DataPart('image/jpeg', imageBytes);

      // final response = await model.generateContent([
      //   Content.multi([prompt, imagePart])
      // ]);
      
      // Simulate a response from the Gemini model
      const jsonResponse = '{"item_1": 10, "item_2": 5}';


      await _sendToBackend(jsonResponse);
      setState(() {
        _analysisResult = "Inventory updated successfully!";
      });

    } catch (e) {
      setState(() {
        _analysisResult = "An error occurred: ${e.toString()}";
      });
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  Future<void> _sendToBackend(String jsonResponse) async {
    try {
      final response = await http.post(
        Uri.parse('http://localhost:8080/api/inventory/update'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({'inventory_json': jsonResponse}),
      );

      if (response.statusCode != 200) {
        setState(() {
          _analysisResult = "Backend update failed: ${response.body}";
        });
      }
    } catch (e) {
      // In a real app, you'd want to handle this more gracefully
      // For example, by checking network connectivity.
      // For this example, we'll just show a generic error.
      if (kDebugMode) {
        print("Error sending to backend: ${e.toString()}");
      }
       setState(() {
          _analysisResult = "Error communicating with backend.";
        });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: Text(widget.title),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            const Text(
              'Welcome to StarSon POS',
              style: TextStyle(fontSize: 24),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: _isLoading ? null : _analyzeInventoryImage,
              child: const Text('Analyze Inventory Image'),
            ),
            const SizedBox(height: 20),
            if (_isLoading)
              const CircularProgressIndicator(),
            if (_analysisResult != null)
              Padding(
                padding: const EdgeInsets.all(16.0),
                child: Text(
                  _analysisResult!,
                  textAlign: TextAlign.center,
                ),
              ),
          ],
        ),
      ),
    );
  }
}
