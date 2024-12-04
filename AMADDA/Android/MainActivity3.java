    package com.example.esass;

    import android.annotation.SuppressLint;
    import android.content.Intent;
    import android.content.SharedPreferences;
    import android.os.Bundle;
    import android.widget.Button;
    import android.widget.CheckBox;
    import android.widget.EditText;

    import androidx.appcompat.app.AppCompatActivity;
    import androidx.core.graphics.Insets;
    import androidx.core.view.ViewCompat;
    import androidx.core.view.WindowInsetsCompat;

    public class MainActivity3 extends AppCompatActivity {

        private EditText itemText;
        private CheckBox checkBoxSun, checkBoxMon, checkBoxTue, checkBoxWed, checkBoxThu, checkBoxFri, checkBoxSat;
        private int itemCount;

        @SuppressLint("MissingInflatedId")
        @Override
        protected void onCreate(Bundle savedInstanceState) {
            super.onCreate(savedInstanceState);
            setContentView(R.layout.activity_main3);

            // 시스템 바 인셋 설정
            ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main3), (v, insets) -> {
                Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
                v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
                return insets;
            });

            // Intent로 item_position 전달받기
            Intent intent = getIntent();
            if (intent != null) {
                itemCount = intent.getIntExtra("item_position", 0);
            }

            // UI 요소 초기화
            itemText = findViewById(R.id.item);
            checkBoxSun = findViewById(R.id.checkBoxSun);
            checkBoxMon = findViewById(R.id.checkBoxMon);
            checkBoxTue = findViewById(R.id.checkBoxTue);
            checkBoxWed = findViewById(R.id.checkBoxWed);
            checkBoxThu = findViewById(R.id.checkBoxThu);
            checkBoxFri = findViewById(R.id.checkBoxFri);
            checkBoxSat = findViewById(R.id.checkBoxSat);

            // 저장된 데이터 복원
            restoreItemData(itemCount);

            // 확인 버튼 동작
            Button confirm = findViewById(R.id.confirm);
            confirm.setOnClickListener(view -> {
                String itemString = itemText.getText().toString();
                String repeatString = makeRepeatString(checkBoxSun, checkBoxMon, checkBoxTue, checkBoxWed, checkBoxThu, checkBoxFri, checkBoxSat);

                // 데이터 저장
                saveItemData(itemCount, itemString, repeatString);

                // 결과 전달
                Intent resultIntent = new Intent();
                resultIntent.putExtra("position", itemCount);
                resultIntent.putExtra("item", itemString);
                resultIntent.putExtra("repeat", repeatString);
                setResult(RESULT_OK, resultIntent); // 결과와 데이터 설정
                finish(); // Activity 종료
            });
        }

        // 반복 요일 문자열 생성
        private String makeRepeatString(CheckBox checkBoxSun, CheckBox checkBoxMon, CheckBox checkBoxTue,
                                        CheckBox checkBoxWed, CheckBox checkBoxThu, CheckBox checkBoxFri, CheckBox checkBoxSat) {
            StringBuilder repeatString = new StringBuilder();

            if (checkBoxSun.isChecked()) repeatString.append("일, ");
            if (checkBoxMon.isChecked()) repeatString.append("월, ");
            if (checkBoxTue.isChecked()) repeatString.append("화, ");
            if (checkBoxWed.isChecked()) repeatString.append("수, ");
            if (checkBoxThu.isChecked()) repeatString.append("목, ");
            if (checkBoxFri.isChecked()) repeatString.append("금, ");
            if (checkBoxSat.isChecked()) repeatString.append("토, ");


            // 마지막 ", " 제거
            if (repeatString.length() > 0) {
                repeatString.setLength(repeatString.length() - 2);
            }

            // 특정 패턴 처리
            String result = repeatString.toString();
            if (result.equals("월, 화, 수, 목, 금")) {
                return "주중";
            } else if (result.equals("일, 토")) {
                return "주말";
            } else if (result.equals("일, 월, 화, 수, 목, 금, 토")) {
                return "매일";
            }

            return result;
        }

        // 데이터 저장
        private void saveItemData(int position, String item, String repeatString) {
            SharedPreferences sharedPreferences = getSharedPreferences("ItemData", MODE_PRIVATE);
            SharedPreferences.Editor editor = sharedPreferences.edit();

            // item_position 별로 데이터를 저장
            editor.putString("item_" + position, item); // 아이템 텍스트
            editor.putString("repeat_" + position, repeatString); // 반복 설정
            editor.apply(); // 저장 실행
        }

        // 데이터 복원
        private void restoreItemData(int position) {
            SharedPreferences sharedPreferences = getSharedPreferences("ItemData", MODE_PRIVATE);

            // 저장된 데이터 가져오기
            String item = sharedPreferences.getString("item_" + position, "");
            String repeatString = sharedPreferences.getString("repeat_" + position, "");

            // EditText에 값 설정
            itemText.setText(item);

            // CheckBox 설정
            if (repeatString.contains("월")) checkBoxMon.setChecked(true);
            if (repeatString.contains("화")) checkBoxTue.setChecked(true);
            if (repeatString.contains("수")) checkBoxWed.setChecked(true);
            if (repeatString.contains("목")) checkBoxThu.setChecked(true);
            if (repeatString.contains("금")) checkBoxFri.setChecked(true);
            if (repeatString.contains("토")) checkBoxSat.setChecked(true);
            if (repeatString.contains("일")) checkBoxSun.setChecked(true);
            if(repeatString.contains("주중")){
                checkBoxMon.setChecked(true);
                checkBoxTue.setChecked(true);
                checkBoxWed.setChecked(true);
                checkBoxThu.setChecked(true);
                checkBoxFri.setChecked(true);
            }
            else if(repeatString.contains("주말")){
                checkBoxSat.setChecked(true);
                checkBoxSun.setChecked(true);
            }
            else if(repeatString.contains("매일")){
                checkBoxSat.setChecked(true);
                checkBoxMon.setChecked(true);
                checkBoxTue.setChecked(true);
                checkBoxWed.setChecked(true);
                checkBoxThu.setChecked(true);
                checkBoxFri.setChecked(true);
                checkBoxSun.setChecked(true);
            }
        }
    }
