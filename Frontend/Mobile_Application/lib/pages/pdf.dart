import 'dart:convert';

import 'package:bottom_bar_with_sheet/bottom_bar_with_sheet.dart';
import 'package:flutter/material.dart';
import 'package:flutter_tts/flutter_tts.dart';
import 'package:http/http.dart' as http;
import 'package:just_audio/just_audio.dart';
import 'package:project/pages/SummaryPage.dart';
// import 'package:project/sample/audio.dart';

class Pdf extends StatefulWidget {
  const Pdf({super.key, required this.text, required this.summary, required this.imp_words});
  final String text;
  final String summary;
  final String imp_words;

  @override
  State<Pdf> createState() => _PdfState();
}

class _PdfState extends State<Pdf> {
  FlutterTts flutterTts = FlutterTts();
  final _bottomBarController = BottomBarWithSheetController(initialIndex: 0);
  bool _isOpen = false;
  final AudioPlayer _audioPlayer = AudioPlayer();
  bool _isPlaying = false;
  double _volume = 1.0;
  double _speed = 2.0;
  final String url = "http://localhost:5000/static/ashif.wav";
  List sentiment = [["happy","happy"]];

  @override
  void initState() {
    super.initState();
    initTTS();
    getSentimentWords();
    _bottomBarController.stream.listen((opened) {
      print(opened);
      setState(() {
        _isOpen = opened;
      });
    });
    _audioPlayer.setUrl(url);
    _audioPlayer.playerStateStream.listen((state) {
      setState(() {
        _isPlaying = state.playing;
      });
    });
  }

  void initTTS() async{
    await flutterTts.setVoice({"name": "Karen", "locale": "en-AU"});
    await flutterTts.setSpeechRate(_speed);
    await flutterTts.setVolume(_volume);
    await flutterTts.setPitch(1.0);
  }

  void _playPause() async{
    _isPlaying = !_isPlaying;
    if (_isPlaying) {
      await flutterTts.speak(widget.text);
    } else {
      await flutterTts.stop();
    }
  }

  void _setVolume(double volume) {
    setState(() {
      _volume = volume;
      _audioPlayer.setVolume(volume);
    });
  }

  void _setSpeed(double speed) {
    setState(() {
      _speed = speed;
      _audioPlayer.setSpeed(speed);
    });
  }

  @override
  void dispose() {
    _audioPlayer.dispose();
    super.dispose();
  }

  void getSentimentWords() async{
    http.Response res = await http.get(Uri.parse("http://localhost:5000/getwords"));
    var decode = jsonDecode(res.body);
    print(decode);
    setState(() {
      sentiment = decode;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Color(0xfff1ffde),
      appBar: AppBar(
        backgroundColor: Color(0xff485551),
        foregroundColor: Colors.white,
        title: Text(
          "Pocket PDF",
          style: TextStyle(
            fontWeight: FontWeight.bold
          ),
        ),
        actions: [
          Padding(
            padding: const EdgeInsets.only(left: 20),
            child: IconButton(
              icon: Icon(Icons.summarize_outlined, size: 35,),
              onPressed: () {
                Navigator.push(context, MaterialPageRoute(builder: (context) => SummaryPage(summary: widget.summary,)));
              },
            ),
          ),
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(15),
        child: SingleChildScrollView(
          child: Text(widget.text)
        ),
      ),
      // floatingActionButton: FloatingActionButton(
      //   backgroundColor: Color(0xff485551),
      //   onPressed: (){
      //     // print("hello");
      //     flutterTts.setSpeechRate(0.5);
      //     flutterTts.setVolume(0.5);
      //     flutterTts.speak(content);
      //     // Navigator.push(
      //     //   context,
      //     //   MaterialPageRoute(
      //     //     builder: (context) => AudioPlayerScreen()
      //     //   ),
      //     // );
      //   },
      //   child: Icon(Icons.play_arrow, color: Colors.white,),
      // )
      bottomNavigationBar: BottomBarWithSheet(
        controller: _bottomBarController,
        mainActionButtonTheme: MainActionButtonTheme(icon: Icon(_isOpen ?Icons.arrow_downward:Icons.arrow_upward, color: Colors.white,)),
        bottomBarTheme: const BottomBarTheme(
          mainButtonPosition: MainButtonPosition.middle,
          decoration: BoxDecoration(
            color: Colors.white, //.......................................
            borderRadius: BorderRadius.vertical(top: Radius.circular(25)),
          ),
          itemIconColor: Colors.grey,
          itemTextStyle: TextStyle(
            color: Colors.grey,
            fontSize: 10.0,
          ),
          selectedItemTextStyle: TextStyle(
            color: Color(0xff485551),
            fontSize: 10.0,
          ),
        ),
        onSelectItem: (index) {
          switch (index) {
            case 0:
              print("Volume Button Pressed");
              break;
            case 1:
              print("Speed Button Pressed");
              break;
          }
        },
        sheetChild: Center(
          child: Container(
            child: SingleChildScrollView(
              child: Column(
                children: [
                  Text('Volume'),
                  Slider(
                    activeColor: Color(0xff485551),
                    value: _volume,
                    onChanged: _setVolume,
                    min: 0.0,
                    max: 1.0,
                  ),
                  Text('Speed'),
                  Slider(
                    activeColor: Color(0xff485551),
                    value: _speed,
                    onChanged: _setSpeed,
                    min: 0.5,
                    max: 2.0,
                  ),
                  SentimentDisplay(sentiment: widget.imp_words,)
                ],
              ),
            ),
          ),
        ),
        items: [
          BottomBarWithSheetItem(
            icon: Icons.volume_up,
            label: 'Volume',
          ),
          BottomBarWithSheetItem(
            icon: Icons.speed,
            label: 'Speed',
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton(
        backgroundColor: Color(0xff485551),
        onPressed: _playPause,
        child: Icon(_isPlaying ? Icons.pause : Icons.play_arrow, color: Colors.white,),
      ),
    );
  }
}

class SentimentDisplay extends StatelessWidget {
  final String sentiment;
  SentimentDisplay({super.key, required this.sentiment});

  @override

  @override
  Widget build(BuildContext context) {
    List<String> parts = sentiment.split('--');
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Wrap(
        spacing: 8.0,
        runSpacing: 8.0,
        children: parts.map((tag) => Chip(
          label: Text(tag),
          backgroundColor: Colors.green,
          labelStyle: TextStyle(color: Colors.black),
        )).toList(),
      ),
    );
  }
}