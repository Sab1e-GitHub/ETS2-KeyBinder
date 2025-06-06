#include "manuallybinder.h"
#include "ui_manuallybinder.h"
#include <QMessageBox>

using namespace std;

ManuallyBinder::ManuallyBinder(QWidget* parent) : QDialog(parent), ui(new Ui::ManuallyBinder) {
    ui->setupUi(this);

    // 往下拉框添加绑定类型
    for (auto item : bindingTypeComboxString) {
        ui->comboBox->addItem(item.second);
    }
    setBindingType(BindingType::lightpark); // 默认选择第2个绑定类型
}

ManuallyBinder::~ManuallyBinder() {
    delete ui;
}

// 设置按键数量
void ManuallyBinder::setKeyCount(size_t count) {
    if (count < 1 || count > DINPUT_MAX_BUTTONS) {
        count = DINPUT_MAX_BUTTONS; // 最大支持DINPUT_MAX_BUTTONS个按键
    }
    keyCount = count; // 按键数量

    ui->comboBox_2->clear(); // 清空下拉框
    for (size_t i = 0; i < keyCount; i++) {
        ui->comboBox_2->addItem(QString::number(i + 1)); // 往下拉框添加按键
    }
    ui->comboBox_2->setCurrentIndex(0); // 重置下拉框选中项
}

void ManuallyBinder::setBindingType(BindingType bindingType) {
    // 设置当前选中的绑定类型
    if (bindingType < BindingType::lightoff || bindingType > BindingType::gearsel2on) {
        bindingType = BindingType::lightpark; // 默认选择第2个绑定类型
    }
    ui->comboBox->setCurrentText(bindingTypeComboxString.at(bindingType)); // 设置当前选中的绑定类型
}

// 清空
void ManuallyBinder::on_pushButton_2_clicked() {
    ui->lineEdit->clear(); // 清空文本框

    actionEffect.clear(); // 清空受影响的按键

    setKeyCount(keyCount); // 重新设置按键数量
}

// 输入
void ManuallyBinder::on_pushButton_clicked() {
    // 获取当前选中的绑定类型
    int bindingTypeIndex = ui->comboBox->currentIndex();
    if (bindingTypeIndex < 0 || bindingTypeIndex >= ui->comboBox->count()) {
        qDebug() << "无效的绑定类型索引";
        return;
    }

    // 获取当前选中的按键
    int keyIndex = ui->comboBox_2->currentText().toInt() - 1; // 转换为0基索引
    if (keyIndex < 0 || keyIndex >= keyCount) {
        qDebug() << "无效的按键索引";
        return;
    }

    actionEffect.insert_or_assign(keyIndex, !ui->comboBox_3->currentIndex()); // 添加按键索引和状态

    QString keyName = "\"按键" + QString::number(keyIndex + 1) + " " + ui->comboBox_3->currentText() + "\""; // 按键名称
    if (ui->lineEdit->text().isEmpty()) {
        ui->lineEdit->setText(keyName); // 设置文本框内容
    } else {
        ui->lineEdit->setText(ui->lineEdit->text() + " 且 " + keyName); // 设置文本框内容
    }

    // 移除下拉框已经输入的按键
    int index = ui->comboBox_2->findText(QString::number(keyIndex + 1));
    if (index != -1) {
        ui->comboBox_2->removeItem(index); // 移除下拉框中的按键
    } else {
        qDebug() << "未找到按键" << keyIndex + 1 << "在下拉框中";
    }
}

void ManuallyBinder::on_pushButton_3_clicked() {
    if (ui->lineEdit->text().isEmpty()) {
        QMessageBox::critical(this, "错误", "请输入按键！");
        return;
    }
    QMessageBox box(QMessageBox::Information, "提示", "是否绑定？");
    box.setStandardButtons(QMessageBox::Yes | QMessageBox::No);
    box.setDefaultButton(QMessageBox::Yes);
    int ret = box.exec();
    if (ret == QMessageBox::Yes) {
        emit keyBound(static_cast<BindingType>(ui->comboBox->currentIndex()), actionEffect); // 发送信号
        close();                                                                             // 关闭窗口
    } else {
        return; // 取消操作
    }
}

// 取消按钮
void ManuallyBinder::on_pushButton_4_clicked() {
    close(); // 关闭窗口
}
