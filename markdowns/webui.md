## Web UI

Start the web ui

```
streamlit run ./assistant/assistant_ui.py
or
./run_assistant_ui.sh
```

It will start a browser in your local machine. `./run_assistant_ui.sh -h` for more info. If you do not want to   start a browser, run:

```
streamlit run ./assistant/assistant_ui.py --server.headless true
or
$ ./run_assistant_ui.sh no
OK: streamlit is installed
Starting streamlit without opening a browser

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8502
  Network URL: http://192.168.1.151:8502
  External URL: http://xxx.xxx.xxx.xxx:8502
```
