import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from model import CharCNN  # Mô hình CNN từ file model.py
from config import Config  # Cấu hình từ file config.py

# Thiết lập thiết bị (GPU hoặc CPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Tải cấu hình
config = Config()

# Định nghĩa transform (tăng cường dữ liệu và chuẩn hóa)
transform = transforms.Compose([
    transforms.Resize((32, 32)),  # Resize ảnh về kích thước 32x32
    transforms.ToTensor(),  # Chuyển ảnh thành tensor
    transforms.Normalize(mean=[0.5], std=[0.5])  # Chuẩn hóa (giả sử ảnh grayscale)
])

# Tải dữ liệu huấn luyện từ thư mục data/characters/
train_dataset = datasets.ImageFolder(root=config.train_data_path, transform=transform)
train_loader = DataLoader(train_dataset, batch_size=config.batch_size, shuffle=True)

# Khởi tạo mô hình
model = CharCNN(num_classes=config.num_classes).to(device)

# Định nghĩa hàm mất mát và tối ưu hóa
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=config.learning_rate)

# Huấn luyện mô hình
num_epochs = config.num_epochs
for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    for i, (images, labels) in enumerate(train_loader):
        images, labels = images.to(device), labels.to(device)

        # Xóa gradient
        optimizer.zero_grad()

        # Forward pass
        outputs = model(images)
        loss = criterion(outputs, labels)

        # Backward pass và tối ưu hóa
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        if (i + 1) % 10 == 0:  # In sau mỗi 10 batch
            print(f"Epoch [{epoch+1}/{num_epochs}], Step [{i+1}/{len(train_loader)}], Loss: {running_loss/10:.4f}")
            running_loss = 0.0

# Lưu mô hình sau khi huấn luyện
torch.save(model.state_dict(), "../../weights/char_cnn.pth")
print("Training finished! Model saved to weights/char_cnn.pth")