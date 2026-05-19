import logging
import ipaddress
from pathlib import Path
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime, timedelta
import socket
class CertificateServer:
    def __init__(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80)) # 连接到一个外部地址以获取本机IP
            local_ip = s.getsockname()[0]
            self.ip_address = local_ip
            s.close()
        except Exception as e:
            logging.error(f"无法获取本机局域网 IP 地址: {e}")
            local_ip = "未知"
        # 证书文件生成在当前 py 文件所在目录，其他类可通过 server.cert_path 访问
        self.cert_path = Path(__file__).parent
        self.key_path = self.cert_path / "key.pem"
        self.cert_file_path = self.cert_path / "cert.pem"
        self.generate_self_signed_certificate()
    def generate_self_signed_certificate(self):
        """
        为指定IP地址生成自签名证书
        """
        try:
            # 生成私钥
            key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
            )

            # 设置证书信息
            subject = issuer = x509.Name([
                x509.NameAttribute(NameOID.COUNTRY_NAME, "CN"),
                x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Beijing"),
                x509.NameAttribute(NameOID.LOCALITY_NAME, "Beijing"),
                x509.NameAttribute(NameOID.ORGANIZATION_NAME, "nieTTS2.0"),
                x509.NameAttribute(NameOID.COMMON_NAME, f"nieTTS2.0 - {self.ip_address}"),
            ])

            # 创建证书
            cert = x509.CertificateBuilder().subject_name(
                subject
            ).issuer_name(
                issuer
            ).public_key(
                key.public_key()
            ).serial_number(
                x509.random_serial_number()
            ).not_valid_before(
                datetime.now().replace(tzinfo=None)
            ).not_valid_after(
                datetime.now().replace(tzinfo=None) + timedelta(days=365)
            ).add_extension(
                x509.SubjectAlternativeName([
                    x509.DNSName("localhost"),
                    x509.DNSName("127.0.0.1"),
                    x509.IPAddress(ipaddress.IPv4Address(self.ip_address)),
                ]),
                critical=False,
            ).sign(key, hashes.SHA256())

            # 保存私钥和证书
            key_path = self.key_path
            cert_path = self.cert_file_path

            with open(key_path, "wb") as f:
                f.write(key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption(),
                ))
            with open(cert_path, "wb") as f:
                f.write(cert.public_bytes(serialization.Encoding.PEM))
            return key_path, cert_path

        except Exception as e:
            logging.error(f"生成自签名证书失败: {e}")
            return None, None