from cayennelpp.lpp_data import LppData


def test_temperature_from_bytes():
    # 01 67 FF D7 = -4.1C
    temp_buf = bytearray([0x01, 0x67, 0xFF, 0xD7])
    temp_dat = LppData.from_bytes(temp_buf)
    assert temp_buf == temp_dat.bytes()


def test_accelerometer_from_bytes():
    # 06 71 04 D2 FB 2E 00 00
    acc_buf = bytearray([0x06, 0x71, 0x04, 0xD2, 0xFB, 0x2E, 0x00, 0x00])
    acc_dat = LppData.from_bytes(acc_buf)
    assert acc_buf == acc_dat.bytes()


def test_gps_from_bytes():
    # 01 88 06 76 5f f2 96 0a 00 03 e8
    gps_buf = bytearray([0x01, 0x88, 0x06, 0x76,
                         0x5f, 0xf2, 0x96, 0x0a,
                         0x00, 0x03, 0xe8])
    gps_dat = LppData.from_bytes(gps_buf)
    assert gps_buf == gps_dat.bytes()
