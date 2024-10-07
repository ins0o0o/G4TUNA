package com.example.week6;

import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.view.MotionEvent;
import android.widget.CompoundButton;
import android.widget.Switch;
import android.widget.TextView;

import androidx.activity.EdgeToEdge;
import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

import org.json.JSONObject;

public class MainActivity extends AppCompatActivity {

    private TextView tv_dist;
    private TextView tv_temp;
    private Switch sw_ADAS;
    private Switch sw_acceleration;
    private Switch sw_brake;
    private Switch sw_auto_ac;
    private Switch sw_airconditioner;
    boolean bt1;
    boolean bt2;
    boolean bt3;
    boolean bt4;
    boolean bt5;
    int temp;
    int distance;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_main);

        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });

        tv_dist = findViewById(R.id.distance);
        tv_temp = findViewById(R.id.temperature);
        sw_ADAS = findViewById(R.id.ADAS);
        sw_acceleration = findViewById(R.id.acceleration);
        sw_brake = findViewById(R.id.brake);
        sw_auto_ac = findViewById(R.id.auto_ac);
        sw_airconditioner = findViewById(R.id.airconditioner);




        sw_ADAS.setOnTouchListener((v, event) -> {
            // 사용자가 스위치를 터치했을 때
            if (event.getAction() == MotionEvent.ACTION_UP) {
                // 스위치 상태를 토글하고 해당 함수 실행
                boolean isChecked = sw_ADAS.isChecked();
                new Thread(() -> fetchData("http://192.168.137.152:5000/toggle_button1")).start();
            }
            return false; // 이벤트를 계속 전달
        });

// 스위치 상태가 변할 때 사용자의 개입으로 인한 상태 변화를 확인
        sw_ADAS.setOnCheckedChangeListener((compoundButton, isChecked) -> {
            // 이곳에서 실행하지 않도록 비워둡니다.
        });
        sw_acceleration.setOnTouchListener((v, event) -> {
            // 사용자가 스위치를 터치했을 때
            if (event.getAction() == MotionEvent.ACTION_UP) {
                // 스위치 상태를 토글하고 해당 함수 실행
                boolean isChecked = sw_acceleration.isChecked();
                new Thread(() -> fetchData("http://192.168.137.152:5000/toggle_button2")).start();
            }
            return false; // 이벤트를 계속 전달
        });

        sw_brake.setOnTouchListener((v, event) -> {
            // 사용자가 스위치를 터치했을 때
            if (event.getAction() == MotionEvent.ACTION_UP) {
                // 스위치 상태를 토글하고 해당 함수 실행
                boolean isChecked = sw_brake.isChecked();
                new Thread(() -> fetchData("http://192.168.137.152:5000/toggle_button3")).start();
            }
            return false; // 이벤트를 계속 전달
        });

        sw_auto_ac.setOnTouchListener((v, event) -> {
            // 사용자가 스위치를 터치했을 때
            if (event.getAction() == MotionEvent.ACTION_UP) {
                // 스위치 상태를 토글하고 해당 함수 실행
                boolean isChecked = sw_auto_ac.isChecked();
                new Thread(() -> fetchData("http://192.168.137.152:5000/toggle_button4")).start();
            }
            return false; // 이벤트를 계속 전달
        });

        sw_airconditioner.setOnTouchListener((v, event) -> {
            // 사용자가 스위치를 터치했을 때
            if (event.getAction() == MotionEvent.ACTION_UP) {
                // 스위치 상태를 토글하고 해당 함수 실행
                boolean isChecked = sw_airconditioner.isChecked();
                new Thread(() -> fetchData("http://192.168.137.152:5000/toggle_button5")).start();
            }
            return false; // 이벤트를 계속 전달
        });
        update thread1 = new update();
        thread1.start();
    }

    // 몰라
    private void fetchData(String url) {
        StringBuilder response = new StringBuilder();
        try {
            URL obj = new URL(url);
            HttpURLConnection con = (HttpURLConnection) obj.openConnection();
            con.setConnectTimeout(30000); // 10초 연결 타임아웃
            con.setReadTimeout(30000);    // 10초 읽기 타임아웃

            con.setRequestMethod("GET");
            int responseCode = con.getResponseCode();
            if (responseCode == HttpURLConnection.HTTP_OK) {
                BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
                String inputLine;
                while ((inputLine = in.readLine()) != null) {
                    response.append(inputLine);
                }
                in.close();
            } else {
                response.append("Error: ").append(responseCode);
            }

        } catch (Exception e) {
            e.printStackTrace();
            response.append("IO error");
        }
    }

    class update extends Thread {
        Message message;

        public void run() {
            while (true) {
                StringBuilder response = new StringBuilder();  // 반복 시 response 초기화
                try {
                    String url = "http://192.168.137.152:5000";
                    URL obj = new URL(url);
                    HttpURLConnection con = (HttpURLConnection) obj.openConnection();
                    con.setConnectTimeout(30000); // 10초 연결 타임아웃
                    con.setReadTimeout(30000);    // 10초 읽기 타임아웃

                    con.setRequestMethod("GET");
                    int responseCode = con.getResponseCode();
                    if (responseCode == HttpURLConnection.HTTP_OK) {
                        BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
                        String inputLine;
                        while ((inputLine = in.readLine()) != null) {
                            response.append(inputLine);
                        }
                        in.close();
                    } else {
                        response.append("Error: ").append(responseCode);
                    }

                    // JSON 파싱
                    JSONObject jsonResponse = new JSONObject(response.toString());
                    bt1 = jsonResponse.getBoolean("button1");
                    bt2 = jsonResponse.getBoolean("button2");
                    bt3 = jsonResponse.getBoolean("button3");
                    bt4 = jsonResponse.getBoolean("button4");
                    bt5 = jsonResponse.getBoolean("button5");
                    temp = jsonResponse.getInt("temperature");
                    distance = jsonResponse.getInt("distance");

                    // Handler로 메인 스레드에 메시지 보내기
                    message = handler.obtainMessage(1);
                    handler.sendMessage(message);

                    // 일정 시간 대기 (예: 5초)
                    Thread.sleep(100);

                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        }
    }

    private final Handler handler = new Handler(new Handler.Callback() {
        @Override
        public boolean handleMessage(@NonNull Message message) {
            if(message.what == 1){
                StringBuilder temp_string = new StringBuilder();
                StringBuilder dist_string = new StringBuilder();
                temp_string.append("온도 : ");
                temp_string.append(String.valueOf(temp));
                temp_string.append("°C");
                dist_string.append("거리 : ");
                dist_string.append(String.valueOf(distance));
                dist_string.append("cm");
                sw_ADAS.setChecked(bt1);
                sw_acceleration.setChecked(bt2);
                sw_brake.setChecked(bt3);
                sw_auto_ac.setChecked(bt4);
                sw_airconditioner.setChecked(bt5);
                tv_temp.setText(temp_string);
                tv_dist.setText(dist_string);
            }

            return true;
        }
    });

}
