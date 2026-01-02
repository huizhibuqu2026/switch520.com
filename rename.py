import os
import re
from datetime import datetime

class BatchRename:
    """
    批量修改文件名工具类
    """
    
    @staticmethod
    def add_prefix_suffix(folder_path, prefix="", suffix="", keep_extension=True):
        """
        给文件名添加前缀和/或后缀
        
        Args:
            folder_path: 文件夹路径
            prefix: 要添加的前缀
            suffix: 要添加的后缀（在扩展名之前）
            keep_extension: 是否保留原文件扩展名
        """
        if not os.path.exists(folder_path):
            print(f"文件夹不存在: {folder_path}")
            return
        
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        
        for filename in files:
            if keep_extension:
                # 分离文件名和扩展名
                name, ext = os.path.splitext(filename)
                new_name = f"{prefix}{name}{suffix}{ext}"
            else:
                new_name = f"{prefix}{filename}{suffix}"
            
            old_path = os.path.join(folder_path, filename)
            new_path = os.path.join(folder_path, new_name)
            
            # 避免重名冲突
            counter = 1
            while os.path.exists(new_path) and new_path != old_path:
                if keep_extension:
                    new_name = f"{prefix}{name}{suffix}_{counter}{ext}"
                else:
                    new_name = f"{prefix}{filename}{suffix}_{counter}"
                new_path = os.path.join(folder_path, new_name)
                counter += 1
            
            try:
                os.rename(old_path, new_path)
                print(f"✓ 已重命名: {filename} -> {new_name}")
            except Exception as e:
                print(f"✗ 重命名失败 {filename}: {e}")
    
    @staticmethod
    def replace_text(folder_path, old_text, new_text, case_sensitive=True):
        """
        替换文件名中的文本
        
        Args:
            folder_path: 文件夹路径
            old_text: 要替换的文本
            new_text: 替换后的文本
            case_sensitive: 是否区分大小写
        """
        if not os.path.exists(folder_path):
            print(f"文件夹不存在: {folder_path}")
            return
        
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        
        for filename in files:
            if case_sensitive:
                new_name = filename.replace(old_text, new_text)
            else:
                # 不区分大小写替换
                pattern = re.compile(re.escape(old_text), re.IGNORECASE)
                new_name = pattern.sub(new_text, filename)
            
            if new_name != filename:
                old_path = os.path.join(folder_path, filename)
                new_path = os.path.join(folder_path, new_name)
                
                # 避免重名冲突
                counter = 1
                base_name, ext = os.path.splitext(new_name)
                while os.path.exists(new_path) and new_path != old_path:
                    new_name = f"{base_name}_{counter}{ext}"
                    new_path = os.path.join(folder_path, new_name)
                    counter += 1
                
                try:
                    os.rename(old_path, new_path)
                    print(f"✓ 已重命名: {filename} -> {new_name}")
                except Exception as e:
                    print(f"✗ 重命名失败 {filename}: {e}")
    
    @staticmethod
    def sequential_rename(folder_path, prefix="file_", start_num=1, digits=3, keep_extension=True):
        """
        顺序编号重命名
        
        Args:
            folder_path: 文件夹路径
            prefix: 文件名前缀
            start_num: 起始编号
            digits: 编号位数（不足补0）
            keep_extension: 是否保留扩展名
        """
        if not os.path.exists(folder_path):
            print(f"文件夹不存在: {folder_path}")
            return
        
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        
        current_num = start_num
        for filename in files:
            if keep_extension:
                _, ext = os.path.splitext(filename)
                new_name = f"{prefix}{str(current_num).zfill(digits)}{ext}"
            else:
                new_name = f"{prefix}{str(current_num).zfill(digits)}"
            
            old_path = os.path.join(folder_path, filename)
            new_path = os.path.join(folder_path, new_name)
            
            try:
                os.rename(old_path, new_path)
                print(f"✓ 已重命名: {filename} -> {new_name}")
                current_num += 1
            except Exception as e:
                print(f"✗ 重命名失败 {filename}: {e}")
    
    @staticmethod
    def remove_text(folder_path, text_to_remove, case_sensitive=True):
        """
        删除文件名中的指定文本
        
        Args:
            folder_path: 文件夹路径
            text_to_remove: 要删除的文本
            case_sensitive: 是否区分大小写
        """
        BatchRename.replace_text(folder_path, text_to_remove, "", case_sensitive)
    
    @staticmethod
    def change_case(folder_path, case_type='lower'):
        """
        修改文件名大小写
        
        Args:
            folder_path: 文件夹路径
            case_type: 大小写类型 ('lower', 'upper', 'title')
        """
        if not os.path.exists(folder_path):
            print(f"文件夹不存在: {folder_path}")
            return
        
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        
        for filename in files:
            name, ext = os.path.splitext(filename)
            
            if case_type == 'lower':
                new_name = name.lower() + ext
            elif case_type == 'upper':
                new_name = name.upper() + ext
            elif case_type == 'title':
                new_name = name.title() + ext
            else:
                print(f"未知的大小写类型: {case_type}")
                return
            
            if new_name != filename:
                old_path = os.path.join(folder_path, filename)
                new_path = os.path.join(folder_path, new_name)
                
                # 避免重名冲突
                counter = 1
                base_name = new_name
                while os.path.exists(new_path) and new_path != old_path:
                    new_name = f"{os.path.splitext(base_name)[0]}_{counter}{ext}"
                    new_path = os.path.join(folder_path, new_name)
                    counter += 1
                
                try:
                    os.rename(old_path, new_path)
                    print(f"✓ 已重命名: {filename} -> {new_name}")
                except Exception as e:
                    print(f"✗ 重命名失败 {filename}: {e}")
    
    @staticmethod
    def remove_special_chars(folder_path, replace_with=""):
        """
        移除文件名中的特殊字符
        
        Args:
            folder_path: 文件夹路径
            replace_with: 替换字符（默认为空，即直接删除）
        """
        if not os.path.exists(folder_path):
            print(f"文件夹不存在: {folder_path}")
            return
        
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        
        for filename in files:
            # 移除特殊字符，只保留字母、数字、中文、下划线、点、空格和连字符
            name, ext = os.path.splitext(filename)
            cleaned_name = re.sub(r'[^\w\u4e00-\u9fa5\s\.\-]', replace_with, name)
            # 合并多个空格和替换字符
            cleaned_name = re.sub(r'\s+', ' ', cleaned_name)
            
            new_name = cleaned_name.strip() + ext
            
            if new_name != filename:
                old_path = os.path.join(folder_path, filename)
                new_path = os.path.join(folder_path, new_name)
                
                # 避免重名冲突
                counter = 1
                base_name = new_name
                while os.path.exists(new_path) and new_path != old_path:
                    new_name = f"{os.path.splitext(base_name)[0]}_{counter}{ext}"
                    new_path = os.path.join(folder_path, new_name)
                    counter += 1
                
                try:
                    os.rename(old_path, new_path)
                    print(f"✓ 已重命名: {filename} -> {new_name}")
                except Exception as e:
                    print(f"✗ 重命名失败 {filename}: {e}")


# 使用示例
def example_usage():
    """使用示例"""
    
    # 1. 添加前缀和后缀
    print("1. 添加前缀和后缀示例:")
    BatchRename.add_prefix_suffix(
        folder_path="./test_files",
        prefix="2024_",
        suffix="_backup"
    )
    
    # 2. 替换文本
    print("\n2. 替换文本示例:")
    BatchRename.replace_text(
        folder_path="./test_files",
        old_text="old",
        new_text="new"
    )
    
    # 3. 顺序编号
    print("\n3. 顺序编号示例:")
    BatchRename.sequential_rename(
        folder_path="./test_files",
        prefix="image_",
        start_num=1,
        digits=3
    )
    
    # 4. 删除文本
    print("\n4. 删除文本示例:")
    BatchRename.remove_text(
        folder_path="./test_files",
        text_to_remove="temp_"
    )
    
    # 5. 修改大小写
    print("\n5. 修改大小写示例:")
    BatchRename.change_case(
        folder_path="./test_files",
        case_type='lower'
    )
    
    # 6. 移除特殊字符
    print("\n6. 移除特殊字符示例:")
    BatchRename.remove_special_chars(
        folder_path="./test_files",
        replace_with="_"
    )


# 命令行接口
def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='批量修改文件名工具')
    parser.add_argument('folder', help='目标文件夹路径')
    
    # 选择操作
    parser.add_argument('--action', choices=['prefix', 'replace', 'sequence', 'remove', 'case', 'clean'],
                       required=True, help='选择操作类型')
    
    # 通用参数
    parser.add_argument('--prefix', help='添加前缀')
    parser.add_argument('--suffix', help='添加后缀')
    parser.add_argument('--old', help='要替换的文本（用于replace/remove操作）')
    parser.add_argument('--new', help='替换后的文本（用于replace操作）')
    parser.add_argument('--case-sensitive', action='store_true', help='是否区分大小写')
    
    # 顺序重命名参数
    parser.add_argument('--start', type=int, default=1, help='起始编号')
    parser.add_argument('--digits', type=int, default=3, help='编号位数')
    
    # 大小写转换参数
    parser.add_argument('--case-type', choices=['lower', 'upper', 'title'], help='大小写类型')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.folder):
        print(f"错误: 文件夹 '{args.folder}' 不存在")
        return
    
    if args.action == 'prefix':
        BatchRename.add_prefix_suffix(args.folder, args.prefix or "", args.suffix or "")
    elif args.action == 'replace':
        if not args.old or not args.new:
            print("错误: replace操作需要--old和--new参数")
            return
        BatchRename.replace_text(args.folder, args.old, args.new, args.case_sensitive)
    elif args.action == 'sequence':
        BatchRename.sequential_rename(args.folder, args.prefix or "file_", 
                                     args.start, args.digits)
    elif args.action == 'remove':
        if not args.old:
            print("错误: remove操作需要--old参数")
            return
        BatchRename.remove_text(args.folder, args.old, args.case_sensitive)
    elif args.action == 'case':
        if not args.case_type:
            print("错误: case操作需要--case-type参数")
            return
        BatchRename.change_case(args.folder, args.case_type)
    elif args.action == 'clean':
        BatchRename.remove_special_chars(args.folder)


if __name__ == "__main__":
    # 直接运行示例
    # example_usage()
    
    # 或者使用命令行参数
    # main()
    
    print("请参考 example_usage() 函数查看使用示例")
    print("或使用命令行: python script.py [folder] --action [action_type] [其他参数]")
