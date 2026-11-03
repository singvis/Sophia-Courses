import os
import openpyxl
from netmiko import ConnectHandler
# 导入特定的异常类，用于捕获设备连接错误
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException

def main():
    # 定义输入文件和输出文件夹名称
    excel_file = "devices.xlsx"
    output_dir = "Config_Backups"

    # 检查输出文件夹是否存在，不存在则创建
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")

    # 尝试读取 Excel 文件，如果文件不存在会报错
    try:
        workbook = openpyxl.load_workbook(excel_file)
        sheet = workbook.active
    except FileNotFoundError:
        print(f"Error: The file '{excel_file}' was not found. Please check the path.")
        return

    # 遍历 Excel 的每一行，跳过第一行表头 (min_row=2)
    for row in sheet.iter_rows(min_row=2, values_only=True):
        # 解包当前行的数据
        device_name, ip, username, password, device_type = row

        # 组装 Netmiko 连接字典
        device_info = {
            'device_type': device_type,
            'host': ip,
            'username': username,
            'password': password,
        }

        print(f"\nConnecting to {device_name} ({ip})...")

        try:
            # 建立 SSH 连接
            net_connect = ConnectHandler(**device_info)
            
            # 执行获取配置的命令（Cisco设备通常用 show running-config）
            config_output = net_connect.send_command('show running-config')
            
            # 保存配置到本地 txt 文件
            file_path = os.path.join(output_dir, f"{device_name}_config.txt")
            with open(file_path, 'w') as file:
                file.write(config_output)
                
            print(f"Successfully saved {device_name} configuration to {file_path}")
            
            # 断开连接
            net_connect.disconnect()

        # 捕获连接超时错误（设备离线、IP填错）
        except NetmikoTimeoutException:
            print(f"Timeout error: {device_name} is unreachable. Skipping.")
        # 捕获认证错误（账号密码错误）
        except NetmikoAuthenticationException:
            print(f"Authentication failed for {device_name}. Skipping.")
        # 捕获其他未知错误
        except Exception as e:
            print(f"An unexpected error occurred with {device_name}: {e}")

    print("\nBackup process completed.")

if __name__ == "__main__":
    main()