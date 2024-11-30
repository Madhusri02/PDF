import 'package:flutter/material.dart';

class SummaryPage extends StatefulWidget {
  const SummaryPage({super.key, required this.summary});
  final String summary;

  @override
  State<SummaryPage> createState() => _SummaryPageState();
}

class _SummaryPageState extends State<SummaryPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Color(0xfff1ffde),
      appBar: AppBar(
        backgroundColor: Color(0xff485551),
        foregroundColor: Colors.white,
        title: Text('Summary'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(15),
        child: Text(widget.summary),
      ),
      // floatingActionButton: FloatingActionButton(
      //   onPressed: () {
      //     // Navigate to the previous page or save the summary to a database
      //   },
      //   child: Icon(Icons.save),
      // ),
    );
  }
}