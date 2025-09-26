Câu hỏi 1: Chạy chương trình trên vài lần. Bạn nhận thấy điều gì? Giải thích!

> Giá trị cuối cùng của resource thay đổi liên tục
>
> Giải thích: Vì `exploit()` được 3 worker thực thi đồng thời mà không đợi nhau, dẫn đến race condition.
>
> Ví dụ 1 timeline:
> - t0: w1 gọi exploit(), w1 getRes() nhận được x
> - t1: w2 gọi exploit(), w2 getRes() nhận được x
> - t2: w1 setRes(x+1), res = x + 1, kết thúc exploit()
> - t3: w3 gọi exploit(), w3 getRes() nhận được x + 1
> - t4: w2 setRes(x+1), res = x + 1, kết thúc exploit()
> - t5: w3 setRes(x+2), res = x + 2, kết thúc exploit()
>
> Đáng ra kết quả mong muốn phải là x + 3

Câu hỏi 2: Thay đổi đoạn mã trong chương trình chạy (phương thức main), thay
đổi kiểu của 3 thực thể worker1-3 thành ThreadedWorkerWithSync. Bạn nhận
thấy sự thay đổi gì ở đầu ra khi chạy chương trình đó khi so sánh với câu hỏi 1?
Giải thích!

> Giá trị cuối cùng của resource luôn là 3000
>
> Giải thích: Vì khi áp dụng `synchronized` thì giờ các worker đợi nhau, w1 phải chạy exploit resource 1000 lần xong
> thì mới đến w2, w3 làm điều tương tự.

Câu hỏi 3: Thay đổi đoạn code của chương trình chạy chính bằng cách thay thế
kiểu của 3 thực thể worker1-3 thành ThreadedWorkerWithLock. Có khác nhau gì
so với đầu ra của câu hỏi 1. Giải thích!

> Giá trị cuối cùng của resource luôn là 3000
>
> Giải thích: Vì khi áp dụng `ReentrantLock` với mỗi lần code trong `exploit` được gọi, cơ chế locking đảm bảo tại 1
> thời điểm thì chỉ có duy nhất 1 worker được thực thi `exploit`, sau khi thực thi xong thì release lock, các worker
> khác chỉ đợi có thể sẽ tiếp tục acquire lock. Khác với cách 2 ở chỗ các worker không đợi nhau chạy xong mà vẫn có thể
> chạy đồng thời, chỉ đợi khi thực sự cần (khi exploit resource)