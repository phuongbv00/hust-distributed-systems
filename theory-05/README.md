Câu hỏi 1: Tại sao phải thực hiện nhân bản dữ liệu?

> - Tăng sẵn sàng và chịu lỗi, khi một replica hỏng vẫn có thành phân tương đương thay thế
> - Giảm độ trễ (CDN)
> - Cân bằng tải, cho phép bảo trì/nâng cấp không downtime
> - Hỗ trợ đọc mở rộng, giảm tải cho thành phần master (cả đọc và ghi).

Câu hỏi 2: 1. Xét một kho dữ liệu phân tán với 5 tiến trình độc lập P1, P2, P3, P4, và P5. Mỗi tiến trình
chỉ tác động lên được bản sao cục bộ riêng của mình. Các bản sao cục bộ kết nối thành kho dữ liệu phân
tán. Xét các tiến trình chỉ tương tác (ghi, đọc) lên thành phần dữ liệu x ở bản sao cục bộ riêng của mình.
Hoạt động của mô hình ở các thời điểm t tương ứng, các thao tác được thực hiện như sau:

- t1: P1 ghi giá trị a
- t2: P3 đọc giá trị a
- t3: P2 ghi giá trị b và P3 ghi giá trị c
- t4: P5 đọc được giá trị b
- t5: P4 và P5 đều đọc được giá trị a
- t6: P4 đọc được giá trị b
- t7: P4 và P5 đọc được giá trị c

(biết rằng ti < ti+1 với i=(0..6)

Câu hỏi:

a) Mô hình trên có thoả mãn nhất quán nhân quả không? Giải thích.

> Phân tích quan hệ nhân quả:
> - P1: write(a) → P3 đọc được a ở t2, sau đó P3 ghi c ở t3 → quan hệ nhân quả: write(a) → write(c).
> - P2: write(b) là thao tác độc lập, không phụ thuộc vào a hay c.
>
> Mô hình thoả mãn nhất quán nhân quả khi: 1 tiến trình thể thấy c, thì nó phải thấy a trước.
>
> Xét 2 tiến trình thấy c ở t7 là P4 và P5, thì chúng đều đã thấy a ở t5 → Mô hình thoả mãn nhất quán nhân quả.

b) Mô hình trên có thoả mãn nhất quán tuần tự không? Giải thích.

> - Xét t4 → t5: P5 đọc được b, sau đó đọc được a tại t5.
> - Nhưng khi xét t5 → t6: P4 đọc được a trước, sau đó lại đọc được b ở t6.
>
> Điều này vi phạm nhất quán tuần tự khi mà không thể xác định 1 thứ tự toàn cục rằng a hay b xảy ra trước.

Câu hỏi 3: Conit là gì? Nếu đặt kích thước Conit quá lớn thì sẽ gây ra vấn đề gì? Tương tự với kích thước
Conit quá nhỏ?
> Conit (consistency unit) là đơn vị đo/bao gói phạm vi nhất quán (theo không gian dữ liệu, thời gian, số lần cập nhật,
> độ lệch giá trị…).
>
> Conit quá lớn: giới hạn nới lỏng quá rộng → sai khác lớn giữa các bản sao, ứng dụng thấy dữ liệu “lệch”, có thể vi
> phạm ràng buộc nghiệp vụ trước khi hòa hợp.
>
> Conit quá nhỏ: đồng bộ/kiểm soát quá chi tiết → chi phí giao tiếp cao, độ trễ tăng, thông lượng giảm, khó mở rộng.

Câu hỏi 4: Tại sao nhất quán nhân quả có tính nhất quán yếu hơn nhất quán tuần tự? Cho ví dụ để làm
rõ điều này.

> Nhất quán tuần tự bắt mọi thao tác xuất hiện theo một thứ tự tuyến tính duy nhất với mọi tiến trình (tôn trọng thứ tự
> chương trình).
>
> Nhất quán nhân quả chỉ bắt buộc bảo toàn thứ tự giữa các thao tác có quan hệ nhân quả (happens-before),
> còn các thao tác độc lập có thể được thấy theo thứ tự khác nhau ở các tiến trình.
>
> Ví dụ: 2 thao tác ghi độc lập x:=1 (P1) và x:=2 (P2) không có quan hệ nhân quả.
> - Causal consistency cho phép tiến trình A thấy 1 rồi 2, trong khi tiến trình B thấy 2 rồi 1. 2 tiến trình A và B
    không có cùng nhận thức về thứ tự xảy ra của 2 sự kiện.
> - Sequential consistency thì tất cả tiến trình phải cùng thấy hoặc (1 → 2) hoặc (2 → 1).

Câu hỏi 5: Vấn đề của mô hình Eventual Consistency là gì? Từ đó đưa ra định nghĩa mô hình nhất quán hướng client.

> Vấn đề: Không đảm bảo thứ tự quan sát tạm thời; có thể thấy dữ liệu cũ, đảo ngược phiên bản, "read-your-writes" và
> "monotonic reads" không được đảm bảo, dễ gây lỗi trải nghiệm/logic phía người dùng.
>
> Nhất quán hướng client (client-centric consistency): tập các đảm bảo theo phiên khách (per-client), như
> Read-Your-Writes, Monotonic Reads, Monotonic Writes, Writes-Follow-Reads, để mỗi người dùng thấy diễn tiến dữ liệu
> nhất quán với chính họ dù toàn hệ thống chỉ eventual.

Câu hỏi 6: Một ngân hàng quyết định sử dụng dịch vụ CDN (Content Delivery Network) của một công ty
mới khởi nghiệp cung cấp.

a) Với bước đặt máy chủ, công ty chọn thuật toán chọn đặt các máy chủ bản sao (replica) dựa trên khoảng
cách với các chi nhánh ngân hàng. Hãy đề xuất thuật toán chọn đặt k replica với N vị trí có thể đặt máy
chủ. Biết rằng đây là thuật toán dựa trên khoảng cách và công ty biết trước các vị trí các chi nhánh ngân
hàng.

> Đề xuất: k-center dựa trên khoảng cách, sử dụng heuristic greedy.
> Cụ thể:
> - (1) Khởi tạo chọn vị trí có tổng khoảng cách đến các chi nhánh nhỏ nhất;
> - (2) Lặp với k-1 máy chủ còn lại: Tìm chi nhánh được phục vụ tệ nhất → Tìm vị trí máy chủ tốt nhất cho chi nhánh đó →
    Thêm máy chủ mới

b) Với thuật toán để quản lý nội dung dữ liệu ở các replica, công ty quyết định chọn thuật toán dựa trên
bản sao kích hoạt bởi server (server-initiated replicas). Hãy mô tả cơ chế đó với việc xem xét một đơn vị
dữ liệu X là thông tin tài khoản một người dùng cùng với 2 ngưỡng là del(X) và rep(X).

> TH1: Khi một bản sao X được truy cập lần đầu tại một vùng mới (1) hoặc tần suất/độ trễ truy cập vượt ngưỡng rep(X) ở
> một vùng (2), origin server chủ động đẩy/nhân bản X đến các edge/PoP gần vùng đó.
>
> TH2: Nếu tần suất/giá trị truy cập xuống dưới del(X) trong một khoảng thời gian, origin server thu hồi/xóa bản sao để
> tiết kiệm tài nguyên.
>
> TH3: Người dùng cập nhật dữ liệu → chuyển đến origin server để invalidate dữ liệu trên các replica. Tình huống này, để
> đảm bảo nhất quán Read-after-Write, hệ thống sẽ tạm thời bỏ qua CDN cho các yêu cầu đọc dữ liệu đó của chính người
> dùng
> đó trong một khoảng thời gian ngắn (ví dụ: 5-10 giây). Tất cả các yêu cầu đọc trong khoảng thời gian này sẽ được
> chuyển
> thẳng về origin server Điều này đảm bảo họ thấy dữ liệu mới nhất, dù có độ trễ cao hơn một chút.

c) Liên quan đến giao thức đảm bảo nhất quán, công ty quyết định chọn giao thức ghi trên các bản sao
(replicated write), tuy nhiên công ty băn khoăn giữa giao thức nhân bản tích cực và giao thức nhân bản
dựa trên túc số. Bạn hãy giúp công ty lựa chọn giao thức phù hợp bằng việc so sánh 2 giao thức trên với
việc chỉ ra ưu nhược điểm của chúng.

> Nhân bản tích cực (active/primary-copy active replication): mọi replica xử lý ghi (thường qua đồng bộ mạnh hoặc
> primary-order).
> - Ưu: độ trễ đọc/ghi thấp khi đồng bộ tốt, failover nhanh, đơn giản cho đọc.
> - Nhược: cần đồng bộ chặt, chi phí cao, khó mở rộng khi ghi nhiều, dễ xung đột nếu không có thứ tự toàn cục.
>
> Nhân bản dựa trên túc số (quorum-based): ghi/đọc yêu cầu đạt Nw/Nr.
> - Ưu: linh hoạt cân bằng R/W, chịu lỗi tốt (miễn đạt quorum), dễ mở rộng.
> - Nhược: độ trễ phụ thuộc số replica tham gia, có thể phải đọc/ghi nhiều bản, cấu hình Nw, Nr sai có thể gây xung đột
    hoặc giảm sẵn sàng.

Câu hỏi 7: Liên quan đến các mô hình nhất quán hướng dữ liệu và các mô hình nhất quán hướng người dùng:

a. Giải thích vắn tắt ý tưởng của 2 loại mô hình nhất quán hướng dữ liệu trên.

> Hướng dữ liệu: tập trung vào việc định nghĩa các quy tắc và đảm bảo về trạng thái của dữ liệu được chia sẻ trên nhiều
> máy chủ bản sao.
>
> Hướng người dùng: tập trung vào việc đảm bảo trải nghiệm hợp lý và không gây khó hiểu cho một người dùng, chấp nhận
> chưa đạt được sự nhất quán toàn cục trong hệ thống.

b. Một công ty startup mới mở chuyên triển khai thương mại hóa dịch vụ CDN (Content Delivery Network) cho 2 loại hình
dịch vụ là thư điện tử và WWW. Để đảm bảo nhất quán dữ liệu cho 2 loại dịch vụ đó thì tầng middleware sẽ áp dụng mô hình
nhất quán dữ liệu nào (ở câu a) cho mỗi loại dịch vụ trên?

> Email: causal + client-centric (read-your-writes, monotonic) là hợp lý vì thư mới với người gửi/người nhận cần tiến
> triển hợp lý theo thời gian, nhưng chấp nhận trễ đồng bộ toàn cầu.
> WWW tĩnh (nội dung cache): eventual/bounded staleness là đủ; ưu tiên độ trễ thấp và cache hit, cho phép nội dung chậm
> cập nhật trong giới hạn TTL/SLA.

c. Công ty đó triển khai 3000 server bản sao vật lý và chọn hình thức nhân bản dữ liệu dựa trên túc số

(quorum) với Nw = 1600 và Nr = 1100. Vậy hệ thống đó sẽ tránh được xung đột đọc-ghi và xung đột ghi-
ghi hay không? Giải thích.
> Tránh xung đột đọc-ghi: Có, vì Nw + Nr = 2700 > N = 3000? (Điều kiện đúng là Nw + Nr > N). 2700 không > 3000, nên
> KHÔNG đảm bảo giao cắt; có thể xảy ra đọc-ghi xung đột.
> Tránh xung đột ghi-ghi: Không, vì cần Nw > N/2 (đa số) để mọi hai tập ghi giao cắt. 1600 > 1500 nên điều kiện ghi-ghi
> được đảm bảo. Do đó: ghi-ghi an toàn, đọc-ghi không bảo đảm (có thể đọc từ tập không giao cắt với ghi gần nhất).