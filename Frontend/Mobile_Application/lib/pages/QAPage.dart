import 'dart:convert';
import 'dart:io';

import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:project/pages/SummaryPage.dart';

class QAPage extends StatefulWidget {
  const QAPage({super.key});

  @override
  State<QAPage> createState() => _QAPageState();
}

class _QAPageState extends State<QAPage> {
  TextEditingController targetUrl = TextEditingController();
  TextEditingController question = TextEditingController();
  String text = "";

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        backgroundColor: Color(0xfff1ffde),
        appBar: AppBar(
          backgroundColor: Color(0xff485551),
          foregroundColor: Colors.white,
          title: Text('Q&A'),
        ),
        body: Padding(
          padding: const EdgeInsets.all(8.0),
          child: Center(
            child: Container(
              child: Column(
                children: [
                  Container(
                    margin: EdgeInsets.only(
                        top: 10, left: 10, right: 10, bottom: 10),
                    child: TextField(
                      controller: targetUrl,
                      decoration: InputDecoration(
                          filled: true,
                          fillColor: Color(0xffFCF8F3),
                          contentPadding: const EdgeInsets.all(15),
                          hintText: "Enter your url here",
                          hintStyle: TextStyle(color: Colors.black),
                          border: OutlineInputBorder(
                              borderRadius: BorderRadius.circular(10))),
                    ),
                  ),
                  SizedBox(
                    height: 5,
                  ),
                  Container(
                    margin: EdgeInsets.only(
                        top: 10, left: 10, right: 10, bottom: 10),
                    child: TextField(
                      controller: question,
                      decoration: InputDecoration(
                          filled: true,
                          fillColor: Color(0xffFCF8F3),
                          contentPadding: const EdgeInsets.all(15),
                          hintText: "Enter your question here...",
                          hintStyle: TextStyle(color: Colors.black),
                          border: OutlineInputBorder(
                              borderRadius: BorderRadius.circular(10))),
                    ),
                  ),
                  SizedBox(
                    height: 20,
                  ),
                  ElevatedButton(
                      onPressed: () async {
                        String target_url = targetUrl.text;
                        String question_text = question.text;
                        String url = "http://localhost:5000/article";
                        print(target_url + " " + question_text);
                        http.Response response = await http.post(
                          Uri.parse(url),
                          headers: {"Content-Type": "application/json"},
                          body: jsonEncode(
                              {"link": target_url, "question": question_text}),
                        );
                        var decode = await jsonDecode(response.body);
                        setState(() {
                          text = decode["answer"];
                        });
                      },
                      child: Text("Submit"),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Color(0xff485551),
                        foregroundColor: Colors.white
                      ),
                      ),
                  SizedBox(
                    height: 50,
                  ),
                  Padding(
                    padding: const EdgeInsets.all(8.0),
                    child: Text(text),
                  ),
                ],
              ),
            ),
          ),
        ));
  }
}
