import sys
import json
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QLineEdit,
    QTextEdit,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QTreeWidget,
    QTreeWidgetItem,
    QHBoxLayout,
    QSizePolicy,
)


class TaskInputTool(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("周报生成器")
        self.setGeometry(100, 100, 1800, 900)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabels(["周报内容预览"])
        self.tree_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.main_layout.addWidget(self.tree_widget)

        # Summary
        summary_layout = QHBoxLayout()

        self.summary_input = QTextEdit(self)
        self.summary_input.setPlaceholderText("请输入总结（每行一个项目）")
        summary_layout.addWidget(self.summary_input)

        self.update_summary_btn = QPushButton("更新总结", self)
        self.update_summary_btn.clicked.connect(self.update_summary)
        summary_layout.addWidget(self.update_summary_btn)

        self.main_layout.addLayout(summary_layout)

        # Category
        category_layout = QHBoxLayout()

        self.category_input = QLineEdit(self)
        self.category_input.setPlaceholderText("请输入大类名称")
        category_layout.addWidget(self.category_input)

        self.add_category_button = QPushButton("新增大类", self)
        self.add_category_button.clicked.connect(self.add_category)
        category_layout.addWidget(self.add_category_button)

        self.main_layout.addLayout(category_layout)

        # Project
        project_layout = QHBoxLayout()

        self.project_name_input = QLineEdit(self)
        self.project_name_input.setPlaceholderText("请输入项目名称")
        project_layout.addWidget(self.project_name_input)

        self.add_project_button = QPushButton("添加新项目", self)
        self.add_project_button.clicked.connect(self.add_project)
        project_layout.addWidget(self.add_project_button)

        self.main_layout.addLayout(project_layout)

        # Task
        task_layout = QHBoxLayout()

        self.task_name_input = QLineEdit(self)
        self.task_name_input.setPlaceholderText("请输入任务名称")
        task_layout.addWidget(self.task_name_input)

        self.add_task_button = QPushButton("添加任务到当前项目", self)
        self.add_task_button.clicked.connect(self.add_task)
        task_layout.addWidget(self.add_task_button)

        self.main_layout.addLayout(task_layout)

        self.description_input = QTextEdit(self)
        self.description_input.setPlaceholderText("请输入描述（每行一个条目）")
        self.main_layout.addWidget(self.description_input)

        # Function Button
        fuction_layout = QHBoxLayout()

        self.save_button = QPushButton("保存为JSON", self)
        self.save_button.clicked.connect(self.save_to_json)
        fuction_layout.addWidget(self.save_button)

        self.delete_button = QPushButton("删除选中条目", self)
        self.delete_button.clicked.connect(self.delete_item)
        fuction_layout.addWidget(self.delete_button)

        self.main_layout.addLayout(fuction_layout)

    def add_category(self):
        category_name = self.category_input.text().strip()
        if not category_name:
            QMessageBox.warning(self, "警告", "类别不能为空！")
            return
        # 查找或创建类别节点
        category_item = None
        for i in range(self.tree_widget.topLevelItemCount()):
            item = self.tree_widget.topLevelItem(i)
            if item.text(0) == category_name:
                category_item = item
                break

        if not category_item:
            category_item = QTreeWidgetItem([category_name])
            self.tree_widget.addTopLevelItem(category_item)
            QMessageBox.information(self, "信息", "新增大类！")

    def add_project(self):
        category_name = self.category_input.text().strip()
        project_name = self.project_name_input.text().strip()

        if not category_name or not project_name:
            QMessageBox.warning(self, "警告", "类别和项目名称不能为空！")
            return

        # 查找或创建类别节点
        category_item = None
        for i in range(self.tree_widget.topLevelItemCount()):
            item = self.tree_widget.topLevelItem(i)
            if item.text(0) == category_name:
                category_item = item
                break

        if not category_item:
            category_item = QTreeWidgetItem([category_name])
            self.tree_widget.addTopLevelItem(category_item)

        # 检查是否已存在该项目
        for j in range(category_item.childCount()):
            item = category_item.child(j)
            if item.text(0) == project_name:
                QMessageBox.warning(self, "警告", "该项目已存在！")
                return

        # 添加新项目节点
        project_item = QTreeWidgetItem([project_name])
        category_item.addChild(project_item)

    def add_task(self):
        category_name = self.category_input.text().strip()
        project_name = self.project_name_input.text().strip()
        task_name = self.task_name_input.text().strip()
        descriptions = self.description_input.toPlainText().strip().splitlines()

        if not category_name or not project_name or not task_name or not descriptions:
            QMessageBox.warning(
                self, "警告", "类别、项目名称、任务名称和描述不能为空！"
            )
            return

        # 查找对应的项目节点
        project_item = None
        for i in range(self.tree_widget.topLevelItemCount()):
            category_item = self.tree_widget.topLevelItem(i)
            if category_item.text(0) == category_name:
                for j in range(category_item.childCount()):
                    item = category_item.child(j)
                    if item.text(0) == project_name:
                        project_item = item
                        break

            if project_item:
                break

        if not project_item:
            QMessageBox.warning(self, "警告", "未找到该项目，请先添加该项目！")
            return

        # 添加任务节点到项目下
        task_item = None
        for k in range(project_item.childCount()):
            task = project_item.child(k)
            if task.text(0) == task_name:
                task_item = task
                break

        if not task_item:
            task_item = QTreeWidgetItem([task_name])
            project_item.addChild(task_item)

        # 添加描述到任务节点
        self.clear_children(task_item)

        for desc in descriptions:
            if desc:  # 避免空描述
                desc_item = QTreeWidgetItem([desc])
                task_item.addChild(desc_item)

    def save_to_json(self):
        data = {}

        for i in range(self.tree_widget.topLevelItemCount()):
            category_item = self.tree_widget.topLevelItem(i)
            category_name = category_item.text(0)
            projects = []

            for j in range(category_item.childCount()):
                project_item = category_item.child(j)
                project_name = project_item.text(0)
                tasks = []

                for k in range(project_item.childCount()):
                    task_item = project_item.child(k)
                    task_name = task_item.text(0)
                    descriptions = [
                        task_item.child(li).text(0)
                        for li in range(task_item.childCount())
                    ]
                    tasks.append({"task_name": task_name, "descriptions": descriptions})

                projects.append({"project_name": project_name, "tasks": tasks})

            data[category_name] = projects

        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(
            self, "保存文件", "", "JSON Files (*.json);;All Files (*)", options=options
        )

        if file_name:
            with open(file_name, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False)
            QMessageBox.information(self, "成功", "文件已成功保存！")

    def delete_item(self):
        current_item = self.tree_widget.currentItem()

        if current_item is None:
            QMessageBox.warning(self, "警告", "请先选中要删除的条目！")
            return

        # 确认删除操作
        reply = QMessageBox.question(
            self,
            "确认删除",
            "你确定要删除选中的条目吗？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            # 删除选中的条目
            parent_item = current_item.parent()
            if parent_item is None:  # 如果是顶级项，直接删除
                index = self.tree_widget.indexOfTopLevelItem(current_item)
                if index != -1:
                    self.tree_widget.takeTopLevelItem(index)
            else:  # 删除子项
                parent_item.removeChild(current_item)

    def update_summary(self):
        summarys = self.summary_input.toPlainText().strip().splitlines()
        if not summarys:
            QMessageBox.warning(self, "警告", "总结不能为空！")
            return

        # 查找或创建类别节点
        summary_item = None
        for i in range(self.tree_widget.topLevelItemCount()):
            item = self.tree_widget.topLevelItem(i)
            if item.text(0) == "Summary":
                summary_item = item
                break

        if not summary_item:
            summary_item = QTreeWidgetItem(["Summary"])
            self.tree_widget.addTopLevelItem(summary_item)

        self.clear_children(summary_item)

        for summary in summarys:
            if summary:
                desc_item = QTreeWidgetItem([summary])
                summary_item.addChild(desc_item)

    def clear_children(self, item):
        while item.childCount() > 0:
            item.removeChild(item.child(0))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    tool = TaskInputTool()
    tool.show()
    sys.exit(app.exec_())
