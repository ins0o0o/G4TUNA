package com.example.esass;

import android.annotation.SuppressLint;
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.view.View;
import android.widget.Button;
import android.widget.FrameLayout;
import android.widget.ImageButton;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import com.google.android.material.floatingactionbutton.FloatingActionButton;

import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.HashMap;
import java.util.Map;

public class MainActivity extends AppCompatActivity {

    private static final int REQUEST_CODE_EXAMPLE = 1;

    private LinearLayout parentLayout;
    private HashMap<Integer, LinearLayout> layoutMap = new HashMap<>();
    private SharedPreferences sharedPreferences;
    private SharedPreferences.Editor editor;
    private int itemCount = 0;

    private Handler handler = new Handler(Looper.getMainLooper()); // 주기적인 작업 실행을 위한 핸들러

    @SuppressLint("MissingInflatedId")
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

        parentLayout = findViewById(R.id.scroll_linear);

        // SharedPreferences 초기화
        sharedPreferences = getSharedPreferences("ItemData", MODE_PRIVATE);
        editor = sharedPreferences.edit();

        // 이전 데이터 복원
        restoreAllItems();

        FloatingActionButton fab = findViewById(R.id.add_button);
        fab.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                addNewItem(itemCount); // 고유 인덱스 전달
                Intent intent = new Intent(MainActivity.this, MainActivity3.class);
                intent.putExtra("item_position", itemCount);
                startActivityForResult(intent, REQUEST_CODE_EXAMPLE); // Activity 시작
                itemCount++; // 추가된 아이템 수 증가
            }
        });

        ImageButton imageButton = findViewById(R.id.account_bt);
        imageButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(MainActivity.this, MainActivity2.class);
                startActivity(intent);
            }
        });

        startSendingDataToServer();
    }

    private void startSendingDataToServer() {
        new Thread(new Runnable() {
            @Override
            public void run() {
                while (true) {
                    try {
                        // 데이터 전송 로직 실행
                        sendDataToServer();

                        // 1초 대기
                        Thread.sleep(1000);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                        break; // 스레드 중단
                    }
                }
            }
        }).start();
    }

    private void sendDataToServer() {
        StringBuilder response = new StringBuilder();
        try {

            String userName = getSharedPreferences("UserPreferences", MODE_PRIVATE).getString("userName", "");
            String userEmail = getSharedPreferences("UserPreferences", MODE_PRIVATE).getString("userEmail", "");

            if(userName == "" && userEmail =="") return;

            // SharedPreferences에서 모든 데이터 가져오기
            Map<String, ?> allEntries = sharedPreferences.getAll();
            JSONObject jsonObject = new JSONObject();

            for (Map.Entry<String, ?> entry : allEntries.entrySet()) {
                jsonObject.put(entry.getKey(), entry.getValue());
            }

            jsonObject.put("userName",userName);
            jsonObject.put("userEmail",userEmail);

            // Flask 서버 URL 설정
            String serverUrl = "http://192.168.137.223:5000/receive-data"; // Flask 서버 URL
            URL url = new URL(serverUrl);

            // HTTP 연결 설정
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setConnectTimeout(30000); // 연결 타임아웃 30초
            connection.setReadTimeout(30000);    // 읽기 타임아웃 30초
            connection.setRequestMethod("POST");
            connection.setRequestProperty("Content-Type", "application/json; utf-8");
            connection.setDoOutput(true);

            // JSON 데이터 전송
            try (OutputStream os = connection.getOutputStream()) {
                byte[] input = jsonObject.toString().getBytes("utf-8");
                os.write(input, 0, input.length);
            }

            // 응답 코드 확인
            int responseCode = connection.getResponseCode();
            if (responseCode == HttpURLConnection.HTTP_OK) {
                BufferedReader in = new BufferedReader(new InputStreamReader(connection.getInputStream()));
                String inputLine;
                while ((inputLine = in.readLine()) != null) {
                    response.append(inputLine);
                }
                in.close();
                System.out.println("서버 응답: " + response.toString());
            } else {
                System.err.println("데이터 전송 실패. 응답 코드: " + responseCode);
            }

        } catch (Exception e) {
            e.printStackTrace();
            System.err.println("데이터 전송 중 오류 발생");
        }
    }


    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        // 요청 코드 확인
        if (requestCode == REQUEST_CODE_EXAMPLE) {
            if (resultCode == RESULT_OK && data != null) {
                int position = data.getIntExtra("position", -1);
                String item = data.getStringExtra("item");
                String repeat = data.getStringExtra("repeat");
                LinearLayout linearLayout = getLayoutByTag(position);
                LinearLayout middleLayout = (LinearLayout) linearLayout.getChildAt(1);
                TextView textView1 = (TextView)middleLayout.getChildAt(1);
                TextView textView2 = (TextView)middleLayout.getChildAt(2);
                textView1.setText(item);
                textView2.setText(repeat);
                Toast.makeText(this, "받은 데이터: " + item, Toast.LENGTH_SHORT).show();
            } else if (resultCode == RESULT_CANCELED) {
                Toast.makeText(this, "결과 취소됨", Toast.LENGTH_SHORT).show();
            }
        }
    }


    private void addNewItem(int position) {
        // 새로운 LinearLayout 생성
        LinearLayout outerLayout = new LinearLayout(this);
        outerLayout.setLayoutParams(new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                dpToPx(100)
        ));
        outerLayout.setOrientation(LinearLayout.HORIZONTAL);

        // 첫 번째 FrameLayout
        FrameLayout frameLayout1 = new FrameLayout(this);
        frameLayout1.setLayoutParams(new LinearLayout.LayoutParams(
                dpToPx(20),
                LinearLayout.LayoutParams.MATCH_PARENT
        ));
        outerLayout.addView(frameLayout1);

        // 중간 LinearLayout
        LinearLayout middleLayout = new LinearLayout(this);
        middleLayout.setLayoutParams(new LinearLayout.LayoutParams(
                dpToPx(200),
                LinearLayout.LayoutParams.MATCH_PARENT
        ));
        middleLayout.setOrientation(LinearLayout.VERTICAL);

        FrameLayout middleFrameLayout = new FrameLayout(this);
        middleFrameLayout.setLayoutParams(new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                dpToPx(20)
        ));
        middleLayout.addView(middleFrameLayout);

        TextView textView1 = new TextView(this);
        textView1.setId(View.generateViewId());
        textView1.setLayoutParams(new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT
        ));
        textView1.setText("");
        textView1.setTextSize(26);
        middleLayout.addView(textView1);

        TextView textView2 = new TextView(this);
        textView2.setId(View.generateViewId());
        textView2.setLayoutParams(new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.MATCH_PARENT
        ));
        textView2.setText("");
        textView2.setTextSize(16);
        middleLayout.addView(textView2);

        outerLayout.addView(middleLayout);

        // 오른쪽 LinearLayout
        LinearLayout rightLayout = new LinearLayout(this);
        rightLayout.setLayoutParams(new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.MATCH_PARENT
        ));
        rightLayout.setOrientation(LinearLayout.VERTICAL);

        FrameLayout rightFrameLayout = new FrameLayout(this);
        rightFrameLayout.setLayoutParams(new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                dpToPx(25)
        ));
        rightLayout.addView(rightFrameLayout);

        LinearLayout buttonLayout = new LinearLayout(this);
        buttonLayout.setLayoutParams(new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.MATCH_PARENT
        ));
        buttonLayout.setOrientation(LinearLayout.HORIZONTAL);

        Button deleteButton = new Button(this);
        deleteButton.setId(View.generateViewId());
        deleteButton.setLayoutParams(new LinearLayout.LayoutParams(
                dpToPx(95),
                LinearLayout.LayoutParams.WRAP_CONTENT,
                1
        ));
        deleteButton.setText("delete");
        deleteButton.setTextColor(Color.WHITE);
        deleteButton.setBackgroundColor(Color.parseColor("#89CFF4"));
        deleteButton.setOnClickListener(view -> {
            // 1. SharedPreferences에서 해당 position 데이터 삭제
            SharedPreferences sharedPreferences = getSharedPreferences("ItemData", MODE_PRIVATE);
            SharedPreferences.Editor editor = sharedPreferences.edit();
            editor.remove("item_" + position); // item 데이터 삭제
            editor.remove("repeat_" + position); // repeat 데이터 삭제
            editor.apply(); // 저장

            // 2. 부모 레이아웃에서 제거
            parentLayout.removeView(outerLayout);

            // 3. layoutMap에서 해당 position 제거
            layoutMap.remove(position);

            Toast.makeText(this, "아이템이 삭제되었습니다.", Toast.LENGTH_SHORT).show();
        });

        buttonLayout.addView(deleteButton);

        FrameLayout buttonSpacer = new FrameLayout(this);
        buttonSpacer.setLayoutParams(new LinearLayout.LayoutParams(
                dpToPx(10),
                LinearLayout.LayoutParams.MATCH_PARENT,
                1
        ));
        buttonLayout.addView(buttonSpacer);

        Button editButton = new Button(this);
        editButton.setId(View.generateViewId());
        editButton.setLayoutParams(new LinearLayout.LayoutParams(
                dpToPx(95),
                LinearLayout.LayoutParams.WRAP_CONTENT,
                1
        ));
        editButton.setText("edit");
        editButton.setTextColor(Color.WHITE);
        editButton.setBackgroundColor(Color.parseColor("#89CFF4"));
        editButton.setOnClickListener(view -> {
            Intent intent = new Intent(MainActivity.this, MainActivity3.class);
            intent.putExtra("item_position", position);
            startActivityForResult(intent, REQUEST_CODE_EXAMPLE);
        });
        buttonLayout.addView(editButton);

        rightLayout.addView(buttonLayout);

        outerLayout.addView(rightLayout);

        // 구분선 View
        View divider = new View(this);
        divider.setId(View.generateViewId());
        divider.setLayoutParams(new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                dpToPx(1)
        ));
        divider.setBackgroundColor(Color.DKGRAY);

        // 추가된 아이템을 parentLayout에 추가
        parentLayout.addView(outerLayout);
        parentLayout.addView(divider);

        // layoutMap에 추가
        layoutMap.put(position, outerLayout);
    }


    private void restoreAllItems() {
        sharedPreferences = getSharedPreferences("ItemData", MODE_PRIVATE); // SharedPreferences 초기화
        Map<String, ?> allEntries = sharedPreferences.getAll();
        for (Map.Entry<String, ?> entry : allEntries.entrySet()) {
            String key = entry.getKey();
            Object value = entry.getValue();

            // 키가 "item_"로 시작하는 경우에만 처리
            if (key.startsWith("item_")) {
                int position = Integer.parseInt(key.split("_")[1]);
                String item = (String) value;
                String repeat = sharedPreferences.getString("repeat_" + position, "");

                // 새로운 아이템 추가
                addNewItem(position);

                // 추가된 레이아웃에 값 설정
                LinearLayout layout = layoutMap.get(position);
                if (layout != null) {
                    LinearLayout middleLayout = (LinearLayout) layout.getChildAt(1);
                    TextView textView1 = (TextView) middleLayout.getChildAt(1);
                    TextView textView2 = (TextView) middleLayout.getChildAt(2);
                    textView1.setText(item);
                    textView2.setText(repeat);
                }

                // itemCount를 복원된 아이템 수에 맞게 업데이트
                if (position >= itemCount) {
                    itemCount = position + 1;
                }
            }
        }
    }

    private int dpToPx(int dp) {
        float density = getResources().getDisplayMetrics().density;
        return Math.round(dp * density);
    }

    public LinearLayout getLayoutByTag(int tag) {
        return layoutMap.get(tag);
    }
}