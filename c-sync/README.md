Câu hỏi 4: Hoàn thiện file trên (điền vào phần YOUR-CODE-HERE) với một vòng
lặp để tăng biến shared lên một đơn vị trong vòng 5 giây.
(gợi ý: hàm time(NULL) sẽ trả về giá trị thời gian của hệ thống với đơn vị là giây).

> ```c
> while (time(NULL) < end) {
>   shared++;
> }
> ```

Câu hỏi 5: Bây giờ hãy tăng giá trị số luồng và giá trị của số lần giao dịch
NUM_TRANS sau mỗi lần chạy chương trình cho đến khi nào bạn thấy sự khác
nhau giữa giá trị Balance (giá trị còn lại trong tài khoản) và
INIT_BALANCE+credits-debits. Giải thích tại sao lại có sự khác nhau đó.

> Do race condition khi thực hiện `balance = balance + v`, tương tự case thực thi `exploit()` trong bài Java.

Câu hỏi 6: Hãy build và chạy chương trình này. Chạy lặp đi lặp lại đến bao giờ bạn
thấy sự khác nhau giữa 2 giá trị Shared và Expect. Phân tích mã nguồn để hiểu
vấn đề.

> Mặc dù đã có một biến lock để cố gắng bảo vệ biến shared, kết quả cuối cùng vẫn bị sai.
>
> Vấn đề cốt lõi của cơ chế "khóa thô sơ" này nằm ở chỗ việc kiểm tra khóa và thiết lập khóa là hai hành động riêng biệt
> và không phải là một thao tác nguyên tử (non-atomic):
> ```c
> while (lock > 0); //spin until unlocked
> // lỗ hổng nằm ở đây!
> lock = 1; //set lock
> ```
>
> OS có thể tạm dừng một luồng (context switch) ngay sau khi nó thoát khỏi vòng lặp while và trước khi nó kịp thực hiện
> lock = 1;.
>
> Timeline ví dụ:
> t0: Luồng A thực thi while (lock > 0);. Nó thấy lock bằng 0, vì vậy nó thoát khỏi vòng lặp để chuẩn bị đặt khóa.
> t1: Ngay tại thời điểm quan trọng này, hệ điều hành tạm dừng Luồng A và chuyển quyền thực thi cho Luồng B. Luồng A
> chưa kịp chạy dòng lock = 1;.
> t2: Luồng B cũng thực thi while (lock > 0);. Vì Luồng A chưa làm gì cả, lock vẫn bằng 0. Luồng B cũng thoát khỏi vòng
> lặp.
> t3: Luồng B thực thi lock = 1;.

Câu hỏi 7: Bây giờ hãy thay đổi đoạn code của file without-lock.c bằng cách triển
khai cơ chế mutex lock như trên (bạn có thể tạo file mới và đặt tên khác đi như
mutex-lock-banking.c). Chạy chương trình nhiều lần và đánh giá đầu ra. Nó có cải
thiện gì hơn so với naive-lock?

Câu hỏi 8: so sánh và đo đạt thời gian để chứng minh là Fine Locking sẽ nhanh
hơn Coarse Locking.

Câu hỏi 9: chạy chương trình trên và bạn nhận thấy điều gì? Giải thích thông qua
việc phân tích mã nguồn.
