package com.example.esass;

import android.annotation.SuppressLint;

import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;


public class MainActivity2 extends AppCompatActivity {

    private EditText nameEditText, emailEditText;

    // SharedPreferences 키 정의
    private static final String PREF_NAME = "UserPreferences";
    private static final String KEY_NAME = "userName";
    private static final String KEY_EMAIL = "userEmail";

    @SuppressLint("MissingInflatedId")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main2);

        // 시스템 바 인셋 설정
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main2), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });

        // UI 요소 초기화
        nameEditText = findViewById(R.id.nameEditText);
        emailEditText = findViewById(R.id.emailEditText);
        Button save_bt = findViewById(R.id.save);
        Button delete_bt = findViewById(R.id.delete);

        // 저장된 데이터 불러오기
        loadSavedData();

        // 저장 버튼 클릭 리스너
        save_bt.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                saveData();
            }
        });

        // 삭제 버튼 클릭 리스너
        delete_bt.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                sendDeleteRequest();
                deleteData();
            }
        });
    }

    private void sendDeleteRequest() {
        new Thread(() -> {
            try {
                String serverUrl = "http://192.168.137.223:5000/receive-data";

                // JSON 데이터 생성
                JSONObject jsonObject = new JSONObject();
                jsonObject.put("name", nameEditText.getText().toString().trim());
                jsonObject.put("email", emailEditText.getText().toString().trim());
                jsonObject.put("delete", true); // delete 상태를 true로 설정

                // HTTP 연결 설정
                URL url = new URL(serverUrl);
                HttpURLConnection connection = (HttpURLConnection) url.openConnection();
                connection.setRequestMethod("POST");
                connection.setRequestProperty("Content-Type", "application/json; utf-8");
                connection.setDoOutput(true);

                // JSON 데이터 전송
                try (OutputStream os = connection.getOutputStream()) {
                    byte[] input = jsonObject.toString().getBytes("utf-8");
                    os.write(input, 0, input.length);
                }

                int responseCode = connection.getResponseCode();
                if (responseCode == HttpURLConnection.HTTP_OK) {
                    BufferedReader in = new BufferedReader(new InputStreamReader(connection.getInputStream()));
                    StringBuilder response = new StringBuilder();
                    String inputLine;
                    while ((inputLine = in.readLine()) != null) {
                        response.append(inputLine);
                    }
                    in.close();
                    System.out.println("서버 응답: " + response.toString());
                } else {
                    System.err.println("삭제 요청 실패: 응답 코드 " + responseCode);
                }

            } catch (Exception e) {
                e.printStackTrace();
            }
        }).start();
    }

    // SharedPreferences에 데이터 저장
    private void saveData() {
        // 입력값 가져오기
        String name = nameEditText.getText().toString().trim();
        String email = emailEditText.getText().toString().trim();

        // 입력값 검증
        if (name.isEmpty() || email.isEmpty()) {
            // 경고 메시지 표시
            Toast.makeText(this, "Please fill in both Name and Email fields", Toast.LENGTH_SHORT).show();
            return; // 저장하지 않고 함수 종료
        }

        // SharedPreferences 생성 (MODE_PRIVATE: 앱 내에서만 사용)
        SharedPreferences sharedPreferences = getSharedPreferences(PREF_NAME, MODE_PRIVATE);
        SharedPreferences.Editor editor = sharedPreferences.edit();

        // 입력값 저장
        editor.putString(KEY_NAME, name);
        editor.putString(KEY_EMAIL, email);
        editor.apply();

        // 성공 메시지 표시
        Toast.makeText(this, "Data saved successfully", Toast.LENGTH_SHORT).show();
        finish(); // 팝업 액티비티 종료
    }

    // SharedPreferences에서 데이터 삭제
    private void deleteData() {
        SharedPreferences sharedPreferences = getSharedPreferences(PREF_NAME, MODE_PRIVATE);
        SharedPreferences.Editor editor = sharedPreferences.edit();

        // 현재 저장된 데이터 확인
        String savedName = sharedPreferences.getString(KEY_NAME, null);
        String savedEmail = sharedPreferences.getString(KEY_EMAIL, null);

        if (savedName != null || savedEmail != null) {
            // 데이터 삭제
            editor.remove(KEY_NAME);
            editor.remove(KEY_EMAIL);
            editor.apply();

            nameEditText.setText("");
            emailEditText.setText("");

            /*Toast.makeText(this, "Data deleted successfully", Toast.LENGTH_SHORT).show();*/
        } else {
            Toast.makeText(this, "No data to delete", Toast.LENGTH_SHORT).show();
        }

        finish(); // 팝업 액티비티 종료
    }

    // 저장된 데이터를 불러와서 EditText에 설정
    private void loadSavedData() {
        SharedPreferences sharedPreferences = getSharedPreferences(PREF_NAME, MODE_PRIVATE);

        String savedName = sharedPreferences.getString(KEY_NAME, "");
        String savedEmail = sharedPreferences.getString(KEY_EMAIL, "");

        nameEditText.setText(savedName);
        emailEditText.setText(savedEmail);
    }
}
