import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class client {
    public static void main(String[] args) {
        try {
            // 요청을 보낼 URL 설정
            String url = "http://172.21.10.252:5000/tlqkf";
            URL obj = new URL(url);

            // HTTP 연결 설정
            HttpURLConnection con = (HttpURLConnection) obj.openConnection();
            con.setRequestMethod("GET");

            // 응답 코드 확인
            int responseCode = con.getResponseCode();

            if (responseCode == HttpURLConnection.HTTP_OK) { // 응답 코드가 200일 경우
                BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
                String inputLine;
                StringBuffer response = new StringBuffer();

                // 응답 데이터를 한 줄씩 읽어서 저장
                while ((inputLine = in.readLine()) != null) {
                    response.append(inputLine);
                }
                in.close();

                // 응답 출력
                System.out.println(response.toString());
            } else {
                System.out.println("Error: " + responseCode);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
