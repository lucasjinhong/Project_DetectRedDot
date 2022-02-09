package com.rocky.find_red

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.Button
import android.widget.Toast
import androidx.appcompat.app.AlertDialog
import com.google.gson.Gson
import okhttp3.*
import java.io.IOException

class MainActivity : AppCompatActivity() {
    private lateinit var btn_query: Button
    //定義資料結構存放 Server 回傳的資料
    class MyObject {
        var _id = ""
        var time = ""
        lateinit var records: Array<Record>
        class Record {
            var color = ""
            var value = ""
            var img = ""
        }
    }
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        btn_query = findViewById(R.id.btn_query)
        btn_query.setOnClickListener {
            //關閉按鈕避免再次查詢
            btn_query.isEnabled = false

            //test
            //val json = "{\"_id\":\"61f252aa2b4f97b8c5e2d997\",\"records\":[{\"color\":\"red\",\"value\":420}],\"time\":\"2022-01-27T08:07:06.769Z\"}"
            //val myObject = Gson().fromJson(json, MyObject::class.java)
            //showDialog(myObject)
            //發送請求
            sendRequest()
        }
    }
    //發送請求
    private fun sendRequest() {
        //Data URL
        // url = "http://10.122.10.126:4000/red"
        val url = "http://192.168.0.10:4000/red"
        //建立 Request.Builder 物件，藉由 url()將網址傳入，再建立 Request 物件
        val req = Request.Builder()
            .url(url)
            .build()
        //建立 OkHttpClient 物件，藉由 newCall()發送請求，並在 enqueue()接收回傳
        OkHttpClient().newCall(req).enqueue(object : Callback {
            //發送成功執行此方法
            override fun onResponse(call: Call, response: Response) {
                //使用 response.body?.string()取得 JSON 字串
                val json = response.body?.string()
                //建立 Gson 並使用其 fromJson()方法，將 JSON 字串以 MyObject 格式輸出
                val myObject = Gson().fromJson(json, MyObject::class.java)
                //顯示結果
                showDialog(myObject)
            }
            //發送失敗執行此方法
            override fun onFailure(call: Call, e: IOException) {
                runOnUiThread {
                    //開啟按鈕可再次查詢
                    btn_query.isEnabled = true
                    Toast.makeText(this@MainActivity,
                        "查詢失敗$e", Toast.LENGTH_SHORT).show()
                }
            }
        })
    }
    //顯示結果
    private fun showDialog(myObject: MyObject) {
        //建立一個字串陣列，用於存放 color 與 value 資訊
        val items = arrayOfNulls<String>(myObject.records.size)
        //將 API 資料取出並建立字串，並存放到字串陣列
        myObject.records.forEachIndexed { index, data ->
            items[index] = "color：${data.color}, value：${data.value}"
        }
        //切換到主執行緒將畫面更新
        runOnUiThread {
            //開啟按鈕可再次查詢
            btn_query.isEnabled = true
            //建立 AlertDialog 物件並顯示字串陣列
            AlertDialog.Builder(this@MainActivity)
                .setTitle("查詢結果")
                .setItems(items, null)
                .show()
        }
    }
}