package com.example.week6;

import android.os.Bundle;
import android.view.View;
import android.widget.CompoundButton;
import android.widget.Switch;
import android.widget.TextView;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class MainActivity extends AppCompatActivity {

    private TextView tv_dist;
    private TextView tv_temp;

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
        Switch sw_ADAS = findViewById(R.id.ADAS);

        sw_ADAS.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton compoundButton, boolean isChecked) {
                new Thread(new Runnable() {
                    @Override
                    public void run() {
                        fetchData();
                    }
                }).start();
            }
        });
    }

    // 안드로이드 메인 스레드에서 url 연결은 못한대, 몰라 시벌 스레드로 만들어 
    private void fetchData() {
        StringBuilder response = new StringBuilder();
        try {
            String url = "https://192.168.173.198:5000/tlqkf";
            URL obj = new URL(url);
            HttpURLConnection con = (HttpURLConnection) obj.openConnection();
            con.setConnectTimeout(10000); // 10초 연결 타임아웃
            con.setReadTimeout(10000);    // 10초 읽기 타임아웃

            con.setRequestMethod("GET");
            response.append("^^");
            int responseCode = con.getResponseCode();
            response.append("^^");
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

        // UI 업데이트는 메인 스레드에서 수행해야 하므로 runOnUiThread 사용
        runOnUiThread(() -> tv_dist.setText(response.toString()));
    }
}
