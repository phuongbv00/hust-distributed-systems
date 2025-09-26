# Chapter 4 Theory

Câu hỏi 1: Trình bày 1 ví dụ để mô phỏng vấn đề gặp phải khi các máy tính/tiến trình hoạt động trong hệ
thống phân tán mà không có đồng hộ vật lý dùng chung.

> Ví dụ hệ thống ghi log sự cố. Mỗi máy ghi timestamp cục bộ cho sự kiện. Do clock drift và độ trễ mạng, sắp xếp log "
> theo giờ" có thể đảo lộn quan hệ nhân quả (sự kiện hậu quả xuất hiện trước nguyên nhân), gây khó phân tích.

Câu hỏi 2: Tại sao Lamport lại đề xuất sử dụng đồng hồ logic thay cho đồng hồ vật lý trong hệ phân tán?

> - Đồng hồ vật lý trên các máy khó đồng bộ chính xác do clock drift và độ trễ mạng; NTP chỉ đảm bảo gần
    đúng nên không bảo toàn quan hệ nhân quả giữa các sự kiện.
> - Mục tiêu của hệ phân tán là sắp xếp sự kiện theo quan hệ happens‑before, không nhất thiết theo thời gian thực.
> - Vì vậy, dùng đồng hồ logic giúp xác định thứ tự tổng quát phù hợp với nhân quả.

Câu hỏi 3: Đặc điểm gì của mạng không dây (wireless network) khiến cho thiết kế các giải thuật đồng
bộ khác các kiểu mạng khác?


> - Độ trễ thay đổi lớn, băng thông biến thiên, tỉ lệ mất gói cao; kênh truyền không tin cậy, không đảm bảo FIFO hay thứ
    tự toàn phần.
> - Tranh chấp truy cập môi trường (MAC), va chạm gói; hiện tượng nút ẩn/nút lộ (hidden/exposed terminal) làm khó phát
    hiện xung đột.
> - Liên kết không đối xứng, chất lượng phụ thuộc vị trí/che chắn; thiết bị di động có thể rời/vào mạng (churn) thường
    xuyên.
> - Hạn chế năng lượng khiến giải thuật phải giảm số trao đổi thông điệp và thời gian bật radio.

Câu hỏi 4: Giải thuật Lamport được đưa ra để thực hiện loại trừ lẫn nhau (mutual exclusion). Giải thuật
được mô tả như sau:
Hệ thống có n tiến trình: P1, P2, ... Pn. Có 1 tài nguyên chia sẻ dùng chung gọi là SR (Shared Resource).
Mỗi tiến trình sẽ lưu trữ một hàng đợi queuei để lưu các yêu cầu của các tiến trình khác khi chưa được
thực hiện.
Khi tiến trình Pi muốn truy cập vào SR, nó sẽ quảng bá 1 thông điệp REQUEST(tsi,i) cho tất cả các tiến
trình khác, đồng thời lưu trữ thông điệp đó vào hàng đợi của mình (queuei) trong đó tsi là timestamp của
yêu cầu.
Khi 1 tiến trình Pj nhận được yêu cầu REQUEST(tsi,i) từ tiến trình Pi thì nó đưa yêu cầu đó vào hàng đợi
của mình (queuej) và gửi trả lại cho Pi thông điệp REPLY.
Tiến trình Pi sẽ tự cho phép mình sử dụng SR khi nó kiểm tra thấy yêu cầu của nó nằm ở đầu hàng đợi
queuei và các yêu cầu khác đều có timestamp lớn hơn yêu cầu của chính nó.
Tiến trình Pi, khi không dùng SR nữa sẽ xóa yêu cầu của nó khỏi hàng đợi và quảng bá thông điệp
RELEASE cho tất cả các tiến trình khác.
Khi tiến trình Pj nhận được thông điệp RELEASE từ Pi thì nó sẽ xóa yêu cầu của Pi trong hàng đợi của
nó.
Câu hỏi:

a) Để thực hiện thành công 1 tiến trình vào sử dụng SR, hệ thống cần tổng cộng bao nhiêu thông điệp?

> 3*(n-1) thông điệp: REQUEST, REPLY, RELEASE:
> - REQUEST tới n-1 tiến trình khác để yc acquire SR.
> - REPLY từ n-1 tiến trình khác.
> - RELEASE tới n-1 tiến trình khác sau khi dùng xong SR.

b) Có 1 cách cải thiện thuật toán trên như sau: sau khi Pj gửi yêu cầu REQUEST cho các tiến trình khác
thì nhận được thông điệp REQUEST từ Pi, nếu nó nhận thấy rằng timestamp của REQUEST nó vừa gửi
lớn hơn timestamp của REQUEST của Pi, nó sẽ không gửi thông điệp REPLY cho Pi nữa.
Cải thiện trên có đúng hay không? Và với cải thiện này thì tổng số thông điệp cần để thực hiện thành
công 1 tiến trình vào sử dụng SR là bao nhiêu? Giải thích.

> Trong tình huống này, diễn biến sẽ là:
> - Pi sẽ ko bao giờ nhận dc REPLY từ Pj → đợi (vì theo Lamport phải nhận đủ n-1 REPLY mới được acquire SR)
> - Đồng thời Pj khi gửi REQUEST tới Pi, (do cải thiện ko đề cập đến case này nên mặc định theo Lamport gốc) Pi sẽ REPLY
    với tsi → Pj phải chờ vì tsj > tsi
>
> Vậy là 2 tiến trình chờ nhau ~ Deadlock → cải thiện là không đúng.
>
> Cải thiện đúng phải là thuật toán Ricart-Agrawala, Pj chỉ không gửi REPLY khi mà tsj < tsi hoặc nó đã acquire được SR
> và đang sử dụng. Khi ấy số lượng thông điệp sẽ là 2*(n-1) vì không cần RELEASE nữa, tiến trình sau khi sử dụng xogn SR
> sẽ chỉ cần REPLY các tiến trình trong hàng đợi

Câu hỏi 5: Giải thuật Szymanski được thiết kế để thực hiện loại trừ lẫn nhau. Ý tưởng của giải
thuật đó là xây dựng một phòng chờ (waiting room) và có đường ra và đường vào, tương ứng
với cổng ra và cổng vào. Ban đầu cổng vào sẽ được mở, cổng ra sẽ đóng. Nếu có một nhóm các
tiến trình cùng yêu cầu muốn được sử dụng tài nguyên chung SR (shared resource) thì các tiến
trình đó sẽ được xếp hàng ở cổng vào và lần lượt vào phòng chờ. Khi tất cả đã vào phòng chờ rồi
thì tiến trình cuối cùng vào phòng sẽ đóng cổng vào và mở cổng ra. Sau đó các tiến trình sẽ lần
lượt được sử dụng tài nguyên chung. Tiến trình cuối cùng sử dụng tài nguyên sẽ đóng cổng ra và
mở lại cổng vào.
Mỗi tiến trình Pi sẽ có 1 biến flagi, chỉ tiến trình Pi mới có quyền ghi, còn các tiến trình Pj (j ≠ i)
thì chỉ đọc được. Trạng thái mở hay đóng cổng sẽ được xác định bằng việc đọc giá trị flag của
các tiến trình khác. Mã giả của thuật toán đối với tiến trình i được viết như sau:

```
#Thực hiện vào phòng đợi
flag[i] ← 1
await(all flag[1..N]∈{0,1,2})
flag[i] ← 3
ifany flag[1..N]=1:
flag[i] ← 2
await(any flag[1..N]=4)
flag[i] ← 4
await(all flag[1..i-1]∈{0,1})
#Sử dụng tài nguyên
#...
#Thực hiện giải phóng tài nguyên
await(all flag[i+1..N]∈{0,1,4})
flag[i] ← 0
```

Giải thích ký pháp trong thuật toán:

- await(điều_kiện): chờ đến khi thỏa mãn điều_kiện
- all: tất cả
- any: có bất kỳ 1 cái nào

Câu hỏi:
flag[i] sẽ có 5 giá trị trạng thái từ 0-4. Dựa vào giải thuật trên, 5 giá trị đó mang ý nghĩa tương
ứng nào sau đây (có giải thích):

- Chờ tiến trình khác vào phòng chờ
- Cổng vào được đóng
- Tiến trình i đang ở ngoài phòng chờ
- Rời phòng, mở lại cổng vào nếu không còn ai trong phòng chờ
- Đứng đợi trong phòng chờ

> - 0: Tiến trình i đang ở ngoài phòng chờ. Giải thích: flag=0 là trạng thái nhàn rỗi/ở ngoài; sau khi rời miền găng và
    hoàn tất điều kiện ở cuối, tiến trình hạ cờ về 0 và trở lại ngoài phòng.
> - 1: Đứng đợi trong phòng chờ. Giải thích: tiến trình bày tỏ ý định vào (set 1) và chuẩn bị vào phòng; đây là giai
    đoạn đứng chờ ban đầu theo dõi các cờ khác.
> - 2: Chờ tiến trình khác vào phòng chờ. Giải thích: nếu còn ai ở mức 1 (đang tới), i lùi về 2 để chờ cho nhóm vào đầy
    đủ trước khi đóng cổng vào.
> - 3: Cổng vào được đóng. Giải thích: i chuyển sang 3 để báo hiệu đóng cổng vào (không nhận thêm người vào đợt này)
    trước khi chuyển dòng người sang cổng ra.
> - 4: Rời phòng, mở lại cổng vào nếu không còn ai trong phòng chờ. Giải thích: mức 4 là phía “cổng ra”, xếp hàng theo
    thứ tự id để vào miền găng; khi là người cuối cùng rời phòng (không còn ai ở 2/3), việc hạ cờ về 0 sẽ tương ứng mở
    lại cổng vào cho đợt tiếp theo.