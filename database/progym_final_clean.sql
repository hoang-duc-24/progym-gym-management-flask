-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Máy chủ: 127.0.0.1:3307
-- Thời gian đã tạo: Th6 01, 2026 lúc 10:57 AM
-- Phiên bản máy phục vụ: 10.4.32-MariaDB
-- Phiên bản PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Cơ sở dữ liệu: `progym_final`
--

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `baotrithietbi`
--

DROP TABLE IF EXISTS `baotrithietbi`;
CREATE TABLE `baotrithietbi` (
  `ma_bao_tri` int(11) NOT NULL,
  `ma_thiet_bi` int(11) NOT NULL,
  `ngay_ghi_nhan` date NOT NULL DEFAULT curdate(),
  `noi_dung` varchar(255) NOT NULL,
  `trang_thai_bao_tri` varchar(30) NOT NULL DEFAULT 'CHO_XU_LY',
  `ngay_hoan_thanh` date DEFAULT NULL,
  `ghi_chu` varchar(255) DEFAULT NULL
) ;

--
-- Đang đổ dữ liệu cho bảng `baotrithietbi`
--

INSERT INTO `baotrithietbi` (`ma_bao_tri`, `ma_thiet_bi`, `ngay_ghi_nhan`, `noi_dung`, `trang_thai_bao_tri`, `ngay_hoan_thanh`, `ghi_chu`) VALUES
(1, 3, '2026-05-06', 'Kiểm tra tiếng kêu bất thường và tra dầu cụm ròng rọc.', 'DA_HOAN_THANH', '2026-05-06', 'Đã kiểm tra, máy vận hành ổn định sau bảo trì.'),
(2, 3, '2026-05-13', 'Tra dầu ray trượt và kiểm tra độ êm khi vận hành.', 'DA_HOAN_THANH', '2026-05-13', 'Đã tra dầu, không còn tiếng kêu bất thường.'),
(3, 3, '2026-05-19', 'Bảo dưỡng máy kéo xô do phát sinh tiếng kêu khi sử dụng.', 'DA_HOAN_THANH', '2026-05-19', 'Đã xử lý khô dầu, theo dõi thêm trong các buổi tập tiếp theo.'),
(4, 4, '2026-05-24', 'Thay 3 miếng đệm cao su bị mòn trên bộ tạ tay.', 'DA_HOAN_THANH', '2026-05-25', 'Đã thay đệm, thiết bị sử dụng bình thường.'),
(5, 4, '2026-05-24', 'Hoàn tất kiểm tra và sắp xếp lại bộ tạ tay.', 'DA_HOAN_THANH', '2026-05-24', 'Đã hoàn tất, không phát sinh lỗi thêm.'),
(6, 5, '2026-05-24', 'Bổ sung ốc vít cố định cho máy tập chân.', 'DA_HOAN_THANH', '2026-05-25', 'Đã bổ sung ốc vít và siết lại các điểm cố định.'),
(7, 3, '2026-05-24', 'Tra dầu bảo dưỡng định kỳ cho máy kéo xô.', 'DA_HOAN_THANH', '2026-05-24', 'Đã tra dầu định kỳ, máy hoạt động ổn định.'),
(8, 5, '2026-05-15', 'Kiểm tra và bổ sung ốc vít cho máy tập chân.', 'DA_HOAN_THANH', '2026-05-24', 'Đã bổ sung ốc vít, thiết bị vận hành an toàn.'),
(9, 14, '2026-05-31', 'Tay cầm bị lỏng.', 'DA_HOAN_THANH', '2026-05-31', 'Đã siết lại tay cầm, thiết bị hoạt động ổn định.'),
(10, 6, '2026-06-01', 'Hỏng bàn đạp', 'CHO_XU_LY', NULL, NULL),
(11, 13, '2026-06-01', 'Thanh đòn bị han rỉ', 'CHO_XU_LY', NULL, NULL);

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `checkinout`
--

DROP TABLE IF EXISTS `checkinout`;
CREATE TABLE `checkinout` (
  `ma_check` int(11) NOT NULL,
  `ma_hoi_vien` int(11) NOT NULL,
  `ma_dang_ky` int(11) NOT NULL,
  `ma_lich_tap` int(11) DEFAULT NULL,
  `thoi_gian_check_in` datetime NOT NULL DEFAULT current_timestamp(),
  `thoi_gian_check_out` datetime DEFAULT NULL,
  `loai_checkin` varchar(30) NOT NULL,
  `trang_thai` varchar(30) NOT NULL DEFAULT 'DANG_CHECKIN',
  `ghi_chu` varchar(255) DEFAULT NULL
) ;

--
-- Đang đổ dữ liệu cho bảng `checkinout`
--

INSERT INTO `checkinout` (`ma_check`, `ma_hoi_vien`, `ma_dang_ky`, `ma_lich_tap`, `thoi_gian_check_in`, `thoi_gian_check_out`, `loai_checkin`, `trang_thai`, `ghi_chu`) VALUES
(1, 2, 3, NULL, '2026-05-07 17:30:00', '2026-05-07 19:00:00', 'TU_DO', 'DA_CHECKOUT', 'Check-in tập tự do'),
(2, 1, 2, 1, '2026-03-05 17:50:00', '2026-03-05 18:35:00', 'THEO_LICH_PT', 'DA_CHECKOUT', 'Check-in theo lịch PT, đã hoàn tất buổi tập.'),
(3, 2, 3, NULL, '2026-05-14 11:46:26', '2026-05-14 12:50:26', 'TU_DO', 'DA_CHECKOUT', 'Hội viên hoàn tất buổi tập và check-out tại quầy.'),
(4, 2, 3, NULL, '2026-05-14 11:47:34', '2026-05-14 12:50:34', 'TU_DO', 'DA_CHECKOUT', 'Hội viên hoàn tất buổi tập và check-out tại quầy.'),
(5, 13, 16, NULL, '2026-03-10 15:35:57', '2026-03-10 17:20:57', 'TU_DO', 'DA_CHECKOUT', 'Hội viên hoàn tất buổi tập buổi chiều.'),
(6, 16, 17, NULL, '2026-04-12 15:43:50', '2026-04-12 16:45:30', 'THEO_LICH_PT', 'DA_CHECKOUT', 'Check-in theo lịch PT, đã hoàn tất buổi tập.'),
(7, 16, 17, 8, '2026-04-14 07:15:13', '2026-04-14 08:20:13', 'THEO_LICH_PT', 'DA_CHECKOUT', 'Check-in theo lịch PT, đã hoàn tất buổi tập.'),
(8, 16, 17, NULL, '2026-04-13 07:32:55', '2026-04-13 08:55:55', 'THEO_LICH_PT', 'DA_CHECKOUT', 'Check-in theo lịch PT, đã hoàn tất buổi tập.'),
(9, 2, 3, NULL, '2026-05-16 07:51:53', '2026-05-16 09:05:53', 'TU_DO', 'DA_CHECKOUT', 'Hội viên hoàn tất buổi tập buổi sáng.'),
(10, 13, 16, NULL, '2026-03-12 13:48:42', '2026-03-12 15:10:42', 'TU_DO', 'DA_CHECKOUT', 'Hội viên hoàn tất buổi tập và check-out tại quầy.'),
(11, 1, 1, NULL, '2026-03-15 13:51:09', '2026-03-15 14:45:09', 'TU_DO', 'DA_CHECKOUT', 'Hội viên hoàn tất buổi tập và check-out tại quầy.'),
(12, 17, 18, 11, '2026-04-16 13:54:32', '2026-04-16 15:30:32', 'THEO_LICH_PT', 'DA_CHECKOUT', 'Check-in theo lịch PT, đã hoàn tất buổi tập.'),
(13, 21, 22, NULL, '2026-03-20 20:39:40', '2026-03-20 21:40:40', 'TU_DO', 'DA_CHECKOUT', 'Hội viên tập buổi tối và check-out trước giờ đóng cửa.'),
(14, 17, 18, 13, '2026-04-17 18:25:11', '2026-04-17 19:35:11', 'THEO_LICH_PT', 'DA_CHECKOUT', 'Check-in theo lịch PT, đã hoàn tất buổi tập.'),
(15, 23, 26, NULL, '2026-05-03 07:17:50', '2026-05-03 08:17:39', 'TU_DO', 'DA_CHECKOUT', ''),
(16, 23, 26, NULL, '2026-05-03 08:20:05', '2026-05-03 09:45:05', 'TU_DO', 'DA_CHECKOUT', 'Hội viên hoàn tất buổi tập và check-out tại quầy.'),
(17, 26, 30, NULL, '2026-05-08 18:47:06', '2026-05-08 20:05:06', 'TU_DO', 'DA_CHECKOUT', 'Hội viên hoàn tất buổi tập buổi tối.'),
(18, 27, 31, NULL, '2026-04-10 20:53:53', '2026-04-10 21:40:53', 'TU_DO', 'DA_CHECKOUT', 'Hội viên tập buổi tối và check-out trước giờ đóng cửa.'),
(19, 2, 3, NULL, '2026-05-22 07:15:27', '2026-05-22 08:45:27', 'TU_DO', 'DA_CHECKOUT', 'Hội viên hoàn tất buổi tập buổi sáng.'),
(20, 13, 16, NULL, '2026-03-18 07:34:43', '2026-03-18 09:10:43', 'TU_DO', 'DA_CHECKOUT', 'Hội viên hoàn tất buổi tập và check-out tại quầy.'),
(21, 22, 24, NULL, '2026-04-06 07:35:22', '2026-04-06 09:00:22', 'TU_DO', 'DA_CHECKOUT', 'Hội viên hoàn tất buổi tập và check-out tại quầy.'),
(22, 20, 21, NULL, '2026-03-20 07:35:29', '2026-03-20 09:05:29', 'TU_DO', 'DA_CHECKOUT', 'Hội viên hoàn tất buổi tập và check-out tại quầy.'),
(23, 27, 31, NULL, '2026-04-11 07:35:48', '2026-04-11 08:45:48', 'TU_DO', 'DA_CHECKOUT', 'Hội viên sử dụng gói trải nghiệm, hoàn tất buổi tập.'),
(24, 4, 5, NULL, '2026-04-01 07:35:57', '2026-04-01 08:07:48', 'TU_DO', 'DA_CHECKOUT', ''),
(25, 26, 30, 17, '2026-05-11 07:20:00', '2026-05-11 08:50:00', 'THEO_LICH_PT', 'DA_CHECKOUT', 'Check-in theo lịch PT, đã hoàn tất buổi tập.'),
(26, 2, 3, NULL, '2026-05-24 08:54:54', '2026-05-24 10:20:54', 'TU_DO', 'DA_CHECKOUT', 'Hội viên hoàn tất buổi tập buổi sáng.'),
(27, 28, 32, NULL, '2026-05-09 10:33:56', '2026-05-09 12:05:56', 'TU_DO', 'DA_CHECKOUT', 'Hội viên hoàn tất buổi tập và check-out tại quầy.'),
(28, 33, 40, NULL, '2026-05-31 09:05:22', '2026-05-31 10:30:22', 'TU_DO', 'DA_CHECKOUT', 'Hội viên hoàn tất buổi tập và check-out tại quầy.'),
(29, 24, 27, NULL, '2026-03-12 18:20:00', '2026-03-12 19:35:00', 'TU_DO', 'DA_CHECKOUT', 'Hội viên hoàn tất buổi tập và check-out tại quầy.'),
(30, 24, 27, NULL, '2026-03-26 07:35:00', '2026-03-26 08:45:00', 'TU_DO', 'DA_CHECKOUT', 'Hội viên hoàn tất buổi tập buổi sáng.'),
(31, 24, 27, NULL, '2026-04-11 18:10:00', '2026-04-11 19:30:00', 'TU_DO', 'DA_CHECKOUT', 'Hội viên hoàn tất buổi tập và check-out tại quầy.'),
(32, 24, 27, NULL, '2026-05-07 18:40:00', '2026-05-07 19:55:00', 'TU_DO', 'DA_CHECKOUT', 'Hội viên hoàn tất buổi tập buổi tối.'),
(33, 6, 8, NULL, '2026-03-18 19:00:00', '2026-03-18 20:15:00', 'TU_DO', 'DA_CHECKOUT', 'Hội viên hoàn tất buổi tập buổi tối.'),
(34, 6, 8, NULL, '2026-04-02 18:30:00', '2026-04-02 19:45:00', 'TU_DO', 'DA_CHECKOUT', 'Hội viên hoàn tất buổi tập và check-out tại quầy.'),
(35, 6, 8, NULL, '2026-04-20 07:25:00', '2026-04-20 08:35:00', 'TU_DO', 'DA_CHECKOUT', 'Hội viên hoàn tất buổi tập buổi sáng.'),
(36, 6, 8, NULL, '2026-05-12 18:15:00', '2026-05-12 19:35:00', 'TU_DO', 'DA_CHECKOUT', 'Hội viên hoàn tất buổi tập và check-out tại quầy.'),
(37, 7, 9, NULL, '2026-03-24 17:50:00', '2026-03-24 19:05:00', 'TU_DO', 'DA_CHECKOUT', 'Hội viên hoàn tất buổi tập và check-out tại quầy.'),
(38, 7, 9, NULL, '2026-04-06 18:20:00', '2026-04-06 19:40:00', 'TU_DO', 'DA_CHECKOUT', 'Hội viên hoàn tất buổi tập buổi tối.'),
(39, 7, 9, NULL, '2026-04-24 07:45:00', '2026-04-24 08:55:00', 'TU_DO', 'DA_CHECKOUT', 'Hội viên hoàn tất buổi tập buổi sáng.'),
(40, 7, 9, NULL, '2026-05-15 18:30:00', '2026-05-15 19:45:00', 'TU_DO', 'DA_CHECKOUT', 'Hội viên hoàn tất buổi tập và check-out tại quầy.'),
(41, 8, 10, NULL, '2026-03-29 19:10:00', '2026-03-29 20:30:00', 'TU_DO', 'DA_CHECKOUT', 'Hội viên hoàn tất buổi tập buổi tối.'),
(42, 8, 10, NULL, '2026-04-12 18:00:00', '2026-04-12 19:20:00', 'TU_DO', 'DA_CHECKOUT', 'Hội viên hoàn tất buổi tập và check-out tại quầy.'),
(43, 8, 10, NULL, '2026-04-30 07:30:00', '2026-04-30 08:45:00', 'TU_DO', 'DA_CHECKOUT', 'Hội viên hoàn tất buổi tập buổi sáng.'),
(44, 8, 10, NULL, '2026-05-18 18:20:00', '2026-05-18 19:35:00', 'TU_DO', 'DA_CHECKOUT', 'Hội viên hoàn tất buổi tập và check-out tại quầy.'),
(45, 31, 36, NULL, '2026-05-08 18:15:00', '2026-05-08 19:25:00', 'TU_DO', 'DA_CHECKOUT', 'Hội viên hoàn tất buổi tập và check-out tại quầy.'),
(46, 31, 36, NULL, '2026-05-22 07:40:00', '2026-05-22 08:50:00', 'TU_DO', 'DA_CHECKOUT', 'Hội viên hoàn tất buổi tập buổi sáng.'),
(47, 30, 38, NULL, '2026-05-09 18:30:00', '2026-05-09 19:45:00', 'TU_DO', 'DA_CHECKOUT', 'Hội viên hoàn tất buổi tập buổi tối.'),
(48, 30, 38, NULL, '2026-05-21 18:10:00', '2026-05-21 19:30:00', 'TU_DO', 'DA_CHECKOUT', 'Hội viên hoàn tất buổi tập và check-out tại quầy.'),
(49, 32, 39, NULL, '2026-05-10 07:35:00', '2026-05-10 08:50:00', 'TU_DO', 'DA_CHECKOUT', 'Hội viên hoàn tất buổi tập buổi sáng.'),
(50, 32, 39, NULL, '2026-05-24 18:40:00', '2026-05-24 19:55:00', 'TU_DO', 'DA_CHECKOUT', 'Hội viên hoàn tất buổi tập và check-out tại quầy.'),
(51, 18, 19, NULL, '2026-05-13 18:20:00', '2026-05-13 19:35:00', 'TU_DO', 'DA_CHECKOUT', 'Hội viên hoàn tất buổi tập và check-out tại quầy.'),
(52, 18, 19, NULL, '2026-05-27 07:30:00', '2026-05-27 08:45:00', 'TU_DO', 'DA_CHECKOUT', 'Hội viên hoàn tất buổi tập buổi sáng.'),
(53, 9, 11, NULL, '2026-05-14 18:10:00', '2026-05-14 19:25:00', 'TU_DO', 'DA_CHECKOUT', 'Hội viên hoàn tất buổi tập buổi tối.'),
(54, 9, 11, NULL, '2026-05-28 18:35:00', '2026-05-28 19:50:00', 'TU_DO', 'DA_CHECKOUT', 'Hội viên hoàn tất buổi tập và check-out tại quầy.'),
(55, 1, 2, 2, '2026-03-07 17:50:00', '2026-03-07 19:05:00', 'THEO_LICH_PT', 'DA_CHECKOUT', 'Check-in theo lịch PT, đã hoàn tất buổi tập.'),
(56, 1, 2, 3, '2026-03-11 17:50:00', '2026-03-11 19:05:00', 'THEO_LICH_PT', 'DA_CHECKOUT', 'Check-in theo lịch PT, đã hoàn tất buổi tập.'),
(57, 5, 7, 7, '2026-04-02 08:20:00', '2026-04-02 10:05:00', 'THEO_LICH_PT', 'DA_CHECKOUT', 'Check-in theo lịch PT, đã hoàn tất buổi tập.'),
(58, 11, 13, 18, '2026-04-18 13:20:00', '2026-04-18 15:05:00', 'THEO_LICH_PT', 'DA_CHECKOUT', 'Check-in theo lịch PT, đã hoàn tất buổi tập.'),
(59, 11, 13, 21, '2026-04-23 09:50:00', '2026-04-23 12:05:00', 'THEO_LICH_PT', 'DA_CHECKOUT', 'Check-in theo lịch PT, đã hoàn tất buổi tập.'),
(60, 16, 17, 10, '2026-04-14 17:50:00', '2026-04-14 19:35:00', 'THEO_LICH_PT', 'DA_CHECKOUT', 'Check-in theo lịch PT, đã hoàn tất buổi tập.'),
(61, 16, 17, 15, '2026-04-16 19:50:00', '2026-04-16 21:35:00', 'THEO_LICH_PT', 'DA_CHECKOUT', 'Check-in theo lịch PT, đã hoàn tất buổi tập.'),
(62, 17, 18, 12, '2026-04-18 07:50:00', '2026-04-18 10:05:00', 'THEO_LICH_PT', 'DA_CHECKOUT', 'Check-in theo lịch PT, đã hoàn tất buổi tập.'),
(63, 22, 25, 14, '2026-04-21 17:50:00', '2026-04-21 19:05:00', 'THEO_LICH_PT', 'DA_CHECKOUT', 'Check-in theo lịch PT, đã hoàn tất buổi tập.'),
(64, 26, 30, 16, '2026-05-08 19:20:00', '2026-05-08 20:35:00', 'THEO_LICH_PT', 'DA_CHECKOUT', 'Check-in theo lịch PT, đã hoàn tất buổi tập.'),
(65, 28, 33, 19, '2026-05-11 08:50:00', '2026-05-11 11:05:00', 'THEO_LICH_PT', 'DA_CHECKOUT', 'Check-in theo lịch PT, đã hoàn tất buổi tập.'),
(66, 28, 33, 20, '2026-05-14 09:02:00', '2026-05-14 10:50:00', 'THEO_LICH_PT', 'DA_CHECKOUT', 'Check-in theo lịch PT, đã hoàn tất buổi tập.'),
(67, 30, 35, 24, '2026-05-12 19:20:00', '2026-05-12 21:05:00', 'THEO_LICH_PT', 'DA_CHECKOUT', 'Check-in theo lịch PT, đã hoàn tất buổi tập.'),
(68, 30, 35, 25, '2026-05-12 17:50:00', '2026-05-12 19:05:00', 'THEO_LICH_PT', 'DA_CHECKOUT', 'Check-in theo lịch PT, đã hoàn tất buổi tập.'),
(69, 31, 37, 26, '2026-05-16 06:50:00', '2026-05-16 09:05:00', 'THEO_LICH_PT', 'DA_CHECKOUT', 'Check-in theo lịch PT, đã hoàn tất buổi tập.'),
(70, 25, 28, 27, '2026-03-06 17:50:00', '2026-03-06 19:35:00', 'THEO_LICH_PT', 'DA_CHECKOUT', 'Check-in theo lịch PT, đã hoàn tất buổi tập.'),
(71, 25, 28, 28, '2026-03-13 17:50:00', '2026-03-13 19:35:00', 'THEO_LICH_PT', 'DA_CHECKOUT', 'Check-in theo lịch PT, đã hoàn tất buổi tập.'),
(72, 25, 28, 29, '2026-03-20 17:50:00', '2026-03-20 19:35:00', 'THEO_LICH_PT', 'DA_CHECKOUT', 'Check-in theo lịch PT, đã hoàn tất buổi tập.'),
(73, 3, 4, NULL, '2026-03-08 18:20:00', '2026-03-08 19:35:00', 'TU_DO', 'DA_CHECKOUT', 'Hội viên hoàn tất buổi tập và check-out tại quầy.'),
(74, 3, 4, NULL, '2026-03-22 07:40:00', '2026-03-22 08:55:00', 'TU_DO', 'DA_CHECKOUT', 'Hội viên hoàn tất buổi tập buổi sáng.'),
(75, 3, 4, NULL, '2026-04-12 18:30:00', '2026-04-12 19:45:00', 'TU_DO', 'DA_CHECKOUT', 'Hội viên hoàn tất buổi tập buổi tối.'),
(76, 3, 4, NULL, '2026-05-10 18:10:00', '2026-05-10 19:25:00', 'TU_DO', 'DA_CHECKOUT', 'Hội viên hoàn tất buổi tập và check-out tại quầy.'),
(77, 29, 41, NULL, '2026-05-31 13:45:24', '2026-05-31 15:00:24', 'TU_DO', 'DA_CHECKOUT', 'Hội viên hoàn tất buổi tập và check-out tại quầy.'),
(78, 3, 4, NULL, '2026-05-31 20:07:14', '2026-05-31 22:00:00', 'TU_DO', 'DA_CHECKOUT', 'Tự động đóng do hội viên quên check-out.');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `chitietbaitap`
--

DROP TABLE IF EXISTS `chitietbaitap`;
CREATE TABLE `chitietbaitap` (
  `ma_chi_tiet` int(11) NOT NULL,
  `ma_nhat_ky` int(11) NOT NULL,
  `ten_bai_tap` varchar(150) NOT NULL,
  `so_set` int(11) DEFAULT NULL,
  `so_rep` varchar(50) DEFAULT NULL,
  `muc_ta` decimal(6,2) DEFAULT NULL,
  `don_vi_ta` varchar(20) DEFAULT 'kg',
  `thoi_gian_phut` int(11) DEFAULT NULL,
  `ghi_chu` varchar(255) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp()
) ;

--
-- Đang đổ dữ liệu cho bảng `chitietbaitap`
--

INSERT INTO `chitietbaitap` (`ma_chi_tiet`, `ma_nhat_ky`, `ten_bai_tap`, `so_set`, `so_rep`, `muc_ta`, `don_vi_ta`, `thoi_gian_phut`, `ghi_chu`, `created_at`) VALUES
(1, 1, 'BB bench', 1, '10', 12.00, 'kg', 2, NULL, '2026-05-16 22:43:48'),
(2, 2, 'Barbell Bench Press', 3, '12', 15.00, 'kg', 5, NULL, '2026-05-24 09:12:20'),
(3, 5, 'Barbell Bench Press', 3, '2', 12.00, 'kg', NULL, NULL, '2026-05-24 09:28:02');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `dangkygoitap`
--

DROP TABLE IF EXISTS `dangkygoitap`;
CREATE TABLE `dangkygoitap` (
  `ma_dang_ky` int(11) NOT NULL,
  `ma_hoi_vien` int(11) NOT NULL,
  `ma_goi_tap` int(11) NOT NULL,
  `ngay_dang_ky` date NOT NULL DEFAULT curdate(),
  `ngay_bat_dau` date NOT NULL,
  `ngay_ket_thuc` date NOT NULL,
  `so_buoi_pt_ban_dau` int(11) DEFAULT 0,
  `so_buoi_pt_con_lai` int(11) DEFAULT 0,
  `tong_tien_phai_tra` decimal(12,2) NOT NULL DEFAULT 0.00,
  `trang_thai_thanh_toan` varchar(30) NOT NULL DEFAULT 'CHUA_THANH_TOAN',
  `trang_thai_hieu_luc` varchar(30) NOT NULL DEFAULT 'CHUA_KICH_HOAT',
  `ghi_chu` varchar(255) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp()
) ;

--
-- Đang đổ dữ liệu cho bảng `dangkygoitap`
--

INSERT INTO `dangkygoitap` (`ma_dang_ky`, `ma_hoi_vien`, `ma_goi_tap`, `ngay_dang_ky`, `ngay_bat_dau`, `ngay_ket_thuc`, `so_buoi_pt_ban_dau`, `so_buoi_pt_con_lai`, `tong_tien_phai_tra`, `trang_thai_thanh_toan`, `trang_thai_hieu_luc`, `ghi_chu`, `created_at`) VALUES
(1, 1, 2, '2026-03-15', '2026-03-15', '2026-06-12', 0, 0, 1350000.00, 'DA_THANH_TOAN', 'DANG_HIEU_LUC', 'Gói tập tự do 3 tháng', '2026-05-10 22:25:38'),
(2, 1, 4, '2026-03-01', '2026-03-01', '2026-08-27', 24, 21, 5500000.00, 'DA_THANH_TOAN', 'DANG_HIEU_LUC', 'Gói PT 24 buổi dùng kèm gói tập tự do', '2026-05-10 22:25:38'),
(3, 2, 1, '2026-05-05', '2026-05-05', '2026-06-03', 0, 0, 500000.00, 'DA_THANH_TOAN', 'DANG_HIEU_LUC', 'Gói tập tự do 1 tháng', '2026-05-10 22:25:38'),
(4, 3, 2, '2026-03-03', '2026-03-03', '2026-05-31', 0, 0, 1350000.00, 'DA_THANH_TOAN', 'HET_HAN', 'Gói tập tự do 3 tháng.', '2026-05-10 22:25:38'),
(5, 4, 2, '2026-03-25', '2026-03-25', '2026-06-22', 0, 0, 1350000.00, 'DA_THANH_TOAN', 'DANG_HIEU_LUC', '', '2026-05-11 08:03:53'),
(6, 4, 3, '2026-04-02', '2026-04-02', '2026-06-30', 12, 12, 3000000.00, 'DA_THANH_TOAN', 'DANG_HIEU_LUC', '', '2026-05-11 08:15:27'),
(7, 5, 3, '2026-04-01', '2026-04-01', '2026-06-29', 12, 11, 3000000.00, 'DA_THANH_TOAN', 'DANG_HIEU_LUC', '', '2026-05-11 10:07:10'),
(8, 6, 2, '2026-03-15', '2026-03-15', '2026-06-12', 0, 0, 1350000.00, 'DA_THANH_TOAN', 'DANG_HIEU_LUC', '', '2026-05-11 10:54:28'),
(9, 7, 2, '2026-03-20', '2026-03-20', '2026-06-17', 0, 0, 1350000.00, 'DA_THANH_TOAN', 'DANG_HIEU_LUC', '', '2026-05-11 10:56:59'),
(10, 8, 2, '2026-03-25', '2026-03-25', '2026-06-22', 0, 0, 1350000.00, 'DA_THANH_TOAN', 'DANG_HIEU_LUC', '', '2026-05-11 10:58:32'),
(11, 9, 2, '2026-05-11', '2026-05-11', '2026-08-08', 0, 0, 1350000.00, 'DA_THANH_TOAN', 'DANG_HIEU_LUC', '', '2026-05-11 10:59:35'),
(12, 10, 3, '2026-04-05', '2026-04-05', '2026-07-03', 12, 12, 3000000.00, 'DA_THANH_TOAN', 'DANG_HIEU_LUC', '', '2026-05-11 11:03:59'),
(13, 11, 3, '2026-04-10', '2026-04-10', '2026-07-08', 12, 10, 3000000.00, 'DA_THANH_TOAN', 'DANG_HIEU_LUC', '', '2026-05-11 11:05:19'),
(14, 12, 3, '2026-04-10', '2026-04-10', '2026-07-08', 12, 12, 3000000.00, 'DA_THANH_TOAN', 'DANG_HIEU_LUC', '', '2026-05-11 11:06:16'),
(15, 6, 3, '2026-04-12', '2026-04-12', '2026-07-10', 12, 12, 3000000.00, 'DA_THANH_TOAN', 'DANG_HIEU_LUC', '', '2026-05-11 11:08:44'),
(16, 13, 2, '2026-03-10', '2026-03-10', '2026-06-07', 0, 0, 1350000.00, 'DA_THANH_TOAN', 'DANG_HIEU_LUC', '', '2026-05-11 15:20:43'),
(17, 16, 3, '2026-04-12', '2026-04-12', '2026-07-10', 12, 9, 3000000.00, 'DA_THANH_TOAN', 'DANG_HIEU_LUC', '', '2026-05-11 15:42:22'),
(18, 17, 3, '2026-04-15', '2026-04-15', '2026-07-13', 12, 9, 3000000.00, 'DA_THANH_TOAN', 'DANG_HIEU_LUC', '', '2026-05-12 22:44:41'),
(19, 18, 1, '2026-05-10', '2026-05-10', '2026-06-08', 0, 0, 500000.00, 'DA_THANH_TOAN', 'DANG_HIEU_LUC', '', '2026-05-13 08:18:42'),
(20, 19, 1, '2026-04-13', '2026-04-13', '2026-05-12', 0, 0, 500000.00, 'DA_THANH_TOAN', 'HET_HAN', '', '2026-05-13 08:22:27'),
(21, 20, 2, '2026-03-15', '2026-03-15', '2026-06-12', 0, 0, 1350000.00, 'DA_THANH_TOAN', 'DANG_HIEU_LUC', '', '2026-05-13 08:23:35'),
(22, 21, 2, '2026-03-20', '2026-03-20', '2026-06-17', 0, 0, 1350000.00, 'DA_THANH_TOAN', 'DANG_HIEU_LUC', '', '2026-05-14 20:38:34'),
(23, 21, 3, '2026-03-14', '2026-03-14', '2026-06-11', 12, 12, 3000000.00, 'DA_THANH_TOAN', 'DANG_HIEU_LUC', 'Gói PT đã thanh toán, chưa phát sinh buổi tập hoàn thành.', '2026-05-14 21:49:38'),
(24, 22, 2, '2026-04-01', '2026-04-01', '2026-06-29', 0, 0, 1350000.00, 'DA_THANH_TOAN', 'DANG_HIEU_LUC', '', '2026-05-14 22:00:01'),
(25, 22, 3, '2026-04-20', '2026-04-20', '2026-07-18', 12, 11, 3000000.00, 'DA_THANH_TOAN', 'DANG_HIEU_LUC', '', '2026-05-14 22:00:41'),
(26, 23, 1, '2026-05-03', '2026-05-03', '2026-06-01', 0, 0, 500000.00, 'DA_THANH_TOAN', 'DANG_HIEU_LUC', '', '2026-05-14 22:03:27'),
(27, 24, 2, '2026-03-08', '2026-03-08', '2026-06-05', 0, 0, 1350000.00, 'DA_THANH_TOAN', 'DANG_HIEU_LUC', '', '2026-05-15 08:43:00'),
(28, 25, 4, '2026-03-01', '2026-03-01', '2026-08-27', 24, 21, 5500000.00, 'DA_THANH_TOAN', 'DANG_HIEU_LUC', 'Gói PT đang sử dụng, đã hoàn thành một số buổi tập.', '2026-05-16 22:08:42'),
(29, 26, 1, '2026-05-01', '2026-05-01', '2026-05-30', 0, 0, 500000.00, 'DA_THANH_TOAN', 'HET_HAN', '', '2026-05-16 22:11:32'),
(30, 26, 3, '2026-05-08', '2026-05-08', '2026-08-05', 12, 10, 3000000.00, 'DA_THANH_TOAN', 'DANG_HIEU_LUC', 'Thêm gói PT', '2026-05-16 22:17:30'),
(31, 27, 7, '2026-04-10', '2026-04-10', '2026-04-16', 0, 0, 100000.00, 'DA_THANH_TOAN', 'HET_HAN', 'Gói trải nghiệm sinh viên 7 ngày.', '2026-05-18 20:53:30'),
(32, 28, 1, '2026-05-05', '2026-05-05', '2026-06-03', 0, 0, 500000.00, 'DA_THANH_TOAN', 'DANG_HIEU_LUC', '', '2026-05-19 09:22:03'),
(33, 28, 3, '2026-05-10', '2026-05-10', '2026-08-07', 12, 10, 3000000.00, 'DA_THANH_TOAN', 'DANG_HIEU_LUC', '', '2026-05-19 09:25:21'),
(34, 29, 3, '2026-05-01', '2026-05-01', '2026-07-29', 12, 12, 3000000.00, 'DA_THANH_TOAN', 'DANG_HIEU_LUC', '', '2026-05-24 09:45:55'),
(35, 30, 4, '2026-05-12', '2026-05-12', '2026-11-07', 24, 22, 5500000.00, 'DA_THANH_TOAN', 'DANG_HIEU_LUC', '', '2026-05-24 09:51:43'),
(36, 31, 1, '2026-05-05', '2026-05-05', '2026-06-03', 0, 0, 500000.00, 'DA_THANH_TOAN', 'DANG_HIEU_LUC', '', '2026-05-26 00:06:24'),
(37, 31, 3, '2026-05-16', '2026-05-16', '2026-08-13', 12, 11, 3000000.00, 'DA_THANH_TOAN', 'DANG_HIEU_LUC', '', '2026-05-26 00:06:50'),
(38, 30, 1, '2026-05-06', '2026-05-06', '2026-06-04', 0, 0, 500000.00, 'DA_THANH_TOAN', 'DANG_HIEU_LUC', '', '2026-05-26 00:12:03'),
(39, 32, 1, '2026-05-07', '2026-05-07', '2026-06-05', 0, 0, 500000.00, 'DA_THANH_TOAN', 'DANG_HIEU_LUC', '', '2026-05-26 00:14:06'),
(40, 33, 2, '2026-03-25', '2026-03-25', '2026-06-22', 0, 0, 1350000.00, 'DA_THANH_TOAN', 'DANG_HIEU_LUC', '', '2026-05-29 07:27:26'),
(41, 29, 1, '2026-05-31', '2026-05-31', '2026-06-29', 0, 0, 500000.00, 'DA_THANH_TOAN', 'DANG_HIEU_LUC', '', '2026-05-31 13:36:24');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `goitap`
--

DROP TABLE IF EXISTS `goitap`;
CREATE TABLE `goitap` (
  `ma_goi_tap` int(11) NOT NULL,
  `ten_goi_tap` varchar(100) NOT NULL,
  `loai_goi` varchar(30) NOT NULL,
  `gia_goi` decimal(12,2) NOT NULL DEFAULT 0.00,
  `thoi_han_ngay` int(11) NOT NULL,
  `so_buoi_pt` int(11) DEFAULT 0,
  `mo_ta` varchar(255) DEFAULT NULL,
  `trang_thai_ap_dung` varchar(30) NOT NULL DEFAULT 'DANG_AP_DUNG'
) ;

--
-- Đang đổ dữ liệu cho bảng `goitap`
--

INSERT INTO `goitap` (`ma_goi_tap`, `ten_goi_tap`, `loai_goi`, `gia_goi`, `thoi_han_ngay`, `so_buoi_pt`, `mo_ta`, `trang_thai_ap_dung`) VALUES
(1, 'Gói tập 1 tháng', 'KHONG_PT', 500000.00, 30, 0, 'Gói tập tự do trong 30 ngày.', 'DANG_AP_DUNG'),
(2, 'Gói tập 3 tháng', 'KHONG_PT', 1350000.00, 90, 0, 'Gói tập tự do 3 tháng, phù hợp hội viên tập duy trì.', 'DANG_AP_DUNG'),
(3, 'Gói PT 12 buổi', 'CO_PT', 3000000.00, 90, 12, 'Gói tập cá nhân 12 buổi cùng huấn luyện viên.', 'DANG_AP_DUNG'),
(4, 'Gói PT 24 buổi', 'CO_PT', 5500000.00, 180, 24, 'Gói tập cá nhân 24 buổi cùng huấn luyện viên.', 'DANG_AP_DUNG'),
(5, 'Gói PT 20 buổi cũ', 'CO_PT', 4500000.00, 90, 20, 'Gói PT cũ, hiện không còn mở bán.', 'NGUNG_AP_DUNG'),
(6, 'Gói tập 1 năm', 'KHONG_PT', 2900000.00, 365, 0, 'Gói tập tự do 1 năm, phù hợp hội viên tập lâu dài.', 'DANG_AP_DUNG'),
(7, 'Gói trải nghiệm sinh viên 7 ngày', 'KHONG_PT', 100000.00, 7, 0, 'Gói trải nghiệm ngắn hạn dành cho sinh viên mới đăng ký.', 'DANG_AP_DUNG');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `hoivien`
--

DROP TABLE IF EXISTS `hoivien`;
CREATE TABLE `hoivien` (
  `ma_hoi_vien` int(11) NOT NULL,
  `ho_ten` varchar(100) NOT NULL,
  `ngay_sinh` date DEFAULT NULL,
  `gioi_tinh` varchar(10) DEFAULT NULL,
  `so_dien_thoai` varchar(15) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `dia_chi` varchar(255) DEFAULT NULL,
  `ngay_tham_gia` date NOT NULL DEFAULT curdate(),
  `trang_thai` varchar(30) NOT NULL DEFAULT 'HOAT_DONG',
  `ghi_chu` varchar(255) DEFAULT NULL
) ;

--
-- Đang đổ dữ liệu cho bảng `hoivien`
--

INSERT INTO `hoivien` (`ma_hoi_vien`, `ho_ten`, `ngay_sinh`, `gioi_tinh`, `so_dien_thoai`, `email`, `dia_chi`, `ngay_tham_gia`, `trang_thai`, `ghi_chu`) VALUES
(1, 'Bùi Đức Anh', '1998-03-15', 'NAM', '0913865724', 'duc.anh.bui98@gmail.com', 'Phường Khương Trung, Thanh Xuân, Hà Nội', '2026-03-01', 'HOAT_DONG', 'Tập đều buổi chiều, quan tâm gói có PT.'),
(2, 'Nguyễn Hà My', '2001-07-22', 'NU', '0987426135', 'ha.my.nguyen01@gmail.com', 'Phường Trung Hòa, Cầu Giấy, Hà Nội', '2026-05-02', 'HOAT_DONG', 'Ưu tiên khung giờ sau giờ làm.'),
(3, 'Phạm Quốc Huy', '1999-11-10', 'NAM', '0936812459', 'quoc.huy.pham99@gmail.com', 'Phường Bạch Mai, Hai Bà Trưng, Hà Nội', '2026-03-03', 'HOAT_DONG', 'Mới đăng ký, cần tư vấn thêm lịch tập phù hợp.'),
(4, 'Nguyễn Đức Hải', '2001-02-21', 'NAM', '0989763129', 'haind@gmail.com', 'Thanh Liệt, Hà Nội', '2026-03-25', 'HOAT_DONG', ''),
(5, 'Hoàng Minh Hoàng', '2000-02-23', 'NAM', '0987654333', 'hminhhoang@gmail.com', 'Định Công, Hà Nội', '2026-04-01', 'HOAT_DONG', ''),
(6, 'Bùi Tiến Đạt', '1997-08-19', 'NAM', '0904125786', 'tien.dat.bui97@gmail.com', 'Phường Văn Quán, Hà Đông, Hà Nội', '2026-03-15', 'HOAT_DONG', NULL),
(7, 'Đào Thị Hồng', '1998-12-06', 'NU', '0973258641', 'thi.hong.dao98@gmail.com', 'Phường Định Công, Hoàng Mai, Hà Nội', '2026-03-20', 'HOAT_DONG', NULL),
(8, 'Hoàng Lê Bảo Long', '2000-05-24', 'NAM', '0968142375', 'bao.long.hoang00@gmail.com', 'Phường Kim Giang, Thanh Xuân, Hà Nội', '2026-03-25', 'HOAT_DONG', NULL),
(9, 'Nguyễn Đình Phong', '1996-09-17', 'NAM', '0837596241', 'dinh.phong.nguyen96@gmail.com', 'Phường Phương Liệt, Thanh Xuân, Hà Nội', '2026-05-11', 'HOAT_DONG', NULL),
(10, 'Nguyễn Tiến Dũng', '1995-04-12', 'NAM', '0942186375', 'tien.dung.nguyen95@gmail.com', 'Phường Mỹ Đình 2, Nam Từ Liêm, Hà Nội', '2026-04-05', 'HOAT_DONG', NULL),
(11, 'Lê Hải Nam', '1999-10-28', 'NAM', '0887364512', 'hai.nam.le99@gmail.com', 'Phường Quan Hoa, Cầu Giấy, Hà Nội', '2026-04-10', 'HOAT_DONG', NULL),
(12, 'Trần Mạnh Hùng', '1994-06-03', 'NAM', '0915248763', 'manh.hung.tran94@gmail.com', 'Phường Khương Đình, Thanh Xuân, Hà Nội', '2026-04-10', 'HOAT_DONG', NULL),
(13, 'Bùi Thu Trà', '2005-01-21', 'NU', '0948318970', 'trathubui@gmail.com', 'Nam Từ Liêm, Hà Nội', '2026-03-10', 'HOAT_DONG', ''),
(16, 'Nguyễn Lan Anh', '2001-12-02', 'NAM', '0247197610', 'lanhnguyen@gmail.com', 'Hà Nội', '2026-04-12', 'HOAT_DONG', ''),
(17, 'Nguyễn Mai Chi', '1995-12-21', 'NU', '0482918510', 'maichinguyen@gmail.com', 'Hà Nội', '2026-04-15', 'HOAT_DONG', ''),
(18, 'Lê Phương Chi', '2000-01-12', 'NU', '0731986310', 'chile@gmail.com', 'Ha Noi', '2026-05-10', 'HOAT_DONG', ''),
(19, 'Nguyễn Thị Thanh', '2000-02-21', 'NU', '0938138102', 'thanhnnguyenthi@gmail.com', 'Hà Nội', '2026-04-13', 'HOAT_DONG', NULL),
(20, 'Bùi Đức Trung', '2001-01-21', 'NAM', '0471394110', 'trungducbui@gmail.com', 'Hà Nội', '2026-03-15', 'HOAT_DONG', ''),
(21, 'Ngô Văn Nam', '1995-02-23', 'NAM', '0281938120', 'namngo@gmail.com', 'Hà Nội', '2026-03-14', 'HOAT_DONG', ''),
(22, 'Bùi Đình Long', '2001-11-11', 'NAM', '0826183190', 'longbui21@gmail.com', 'Hà Nội', '2026-04-01', 'HOAT_DONG', ''),
(23, 'Ngô Thị Thu', '2001-01-22', 'NU', '0783121890', 'thu.ngothi01@gmail.com', 'Phường Nguyễn Trãi, Hà Đông, Hà Nội', '2026-05-03', 'HOAT_DONG', NULL),
(24, 'Bùi Thị Ánh', '1990-02-12', 'NU', '0417318291', 'anhbui@gmail.com', 'Hà Nội', '2026-03-08', 'HOAT_DONG', ''),
(25, 'Trần Quốc Đạt', '1997-02-18', 'NAM', '0869472513', 'quoc.dat.tran97@gmail.com', 'Phường Đại Kim, Hoàng Mai, Hà Nội', '2026-03-01', 'HOAT_DONG', NULL),
(26, 'Nguyễn Văn Tài', '2001-02-01', 'NAM', '0981238170', 'van@gmail.com', 'Hà Nội', '2026-05-01', 'HOAT_DONG', NULL),
(27, 'Đào Mạnh Hải', '2004-01-02', 'NAM', '0371192831', 'haimanhdao@gmail.com', 'Nam Từ Liêm, Hà Nội', '2026-04-10', 'NGUNG_HOAT_DONG', 'Kết thúc gói trải nghiệm, chưa tiếp tục đăng ký gói mới.'),
(28, 'Hoàng Minh Đức', '2001-01-21', 'NAM', '0937112810', 'duc@gmail.com', 'Hà Nội', '2026-05-05', 'HOAT_DONG', ''),
(29, 'Lê Tiến Dũng', '2001-02-01', 'NAM', '0927181920', 'dungle@gmail.com', 'Hà Nội', '2026-05-01', 'HOAT_DONG', ''),
(30, 'Ngô Đức Anh', '1990-01-21', 'NAM', '0927192719', 'ducanh@gmail.com', 'Hà Nội', '2026-05-06', 'HOAT_DONG', ''),
(31, 'Trịnh Thu Huyền', '2001-02-21', 'NU', '0937182810', 'huyenthu12@gmail.com', 'Hà Nội', '2026-05-05', 'HOAT_DONG', ''),
(32, 'Ngô Mạnh Hà', '2004-02-21', 'NAM', '0381921093', 'hamanh12@gmail.com', 'Kim Giang, Định Công, Hà Nội', '2026-05-07', 'HOAT_DONG', ''),
(33, 'Đỗ Trung Hiếu', '2001-02-21', 'NAM', '0391918190', 'hieutrung@gmail.com', 'Hà Nội', '2026-03-25', 'HOAT_DONG', '');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `lichtap`
--

DROP TABLE IF EXISTS `lichtap`;
CREATE TABLE `lichtap` (
  `ma_lich_tap` int(11) NOT NULL,
  `ma_phan_cong` int(11) NOT NULL,
  `ngay_tap` date NOT NULL,
  `gio_bat_dau` time NOT NULL,
  `gio_ket_thuc` time NOT NULL,
  `trang_thai_buoi_tap` varchar(30) NOT NULL DEFAULT 'DA_LEN_LICH',
  `ghi_chu` varchar(255) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp()
) ;

--
-- Đang đổ dữ liệu cho bảng `lichtap`
--

INSERT INTO `lichtap` (`ma_lich_tap`, `ma_phan_cong`, `ngay_tap`, `gio_bat_dau`, `gio_ket_thuc`, `trang_thai_buoi_tap`, `ghi_chu`, `created_at`) VALUES
(1, 1, '2026-03-05', '18:00:00', '19:00:00', 'HOAN_THANH', 'Buổi tập đầu tiên', '2026-05-10 22:25:38'),
(2, 1, '2026-03-07', '18:00:00', '19:00:00', 'HOAN_THANH', 'Buổi tập thứ hai', '2026-05-10 22:25:38'),
(3, 2, '2026-03-11', '18:00:00', '19:00:00', 'HOAN_THANH', '', '2026-05-11 10:02:12'),
(4, 4, '2026-04-01', '19:20:00', '20:30:00', 'HUY', '', '2026-05-11 10:09:31'),
(5, 2, '2026-03-13', '07:00:00', '09:00:00', 'HUY', 'Hội viên bị ốm', '2026-05-12 22:11:29'),
(7, 4, '2026-04-02', '08:30:00', '10:00:00', 'HOAN_THANH', '', '2026-05-12 22:23:57'),
(8, 5, '2026-04-14', '07:30:00', '09:00:00', 'HOAN_THANH', '', '2026-05-13 07:14:15'),
(9, 5, '2026-04-14', '18:00:00', '19:00:00', 'HUY', 'Do PT Lan nghỉ, cần phân công PT mới', '2026-05-13 09:46:06'),
(10, 8, '2026-04-14', '18:00:00', '19:30:00', 'HOAN_THANH', '', '2026-05-13 10:21:10'),
(11, 9, '2026-04-16', '14:00:00', '15:30:00', 'HOAN_THANH', '', '2026-05-13 13:53:19'),
(12, 9, '2026-04-18', '08:00:00', '10:00:00', 'HOAN_THANH', '', '2026-05-14 23:22:37'),
(13, 9, '2026-04-17', '18:00:00', '19:00:00', 'HOAN_THANH', '', '2026-05-14 23:24:38'),
(14, 10, '2026-04-21', '18:00:00', '19:00:00', 'HOAN_THANH', '', '2026-05-15 07:34:07'),
(15, 8, '2026-04-16', '20:00:00', '21:30:00', 'HOAN_THANH', '', '2026-05-15 07:39:25'),
(16, 13, '2026-05-08', '19:30:00', '20:30:00', 'HOAN_THANH', '', '2026-05-16 22:37:21'),
(17, 14, '2026-05-11', '07:30:00', '08:45:00', 'HOAN_THANH', 'Đã hoàn thành buổi tập PT buổi sáng.', '2026-05-19 08:06:18'),
(18, 16, '2026-04-18', '13:30:00', '15:00:00', 'HOAN_THANH', 'Đã hoàn thành buổi tập.', '2026-05-19 10:07:07'),
(19, 17, '2026-05-11', '09:00:00', '11:00:00', 'HOAN_THANH', '', '2026-05-21 08:57:32'),
(20, 17, '2026-05-14', '09:12:00', '10:45:00', 'HOAN_THANH', 'Đã hoàn thành buổi tập.', '2026-05-24 09:10:29'),
(21, 16, '2026-04-23', '10:00:00', '12:00:00', 'HOAN_THANH', 'Đã hoàn thành', '2026-05-24 09:42:08'),
(22, 14, '2026-05-17', '08:00:00', '10:00:00', 'HUY', 'Khách bị ốm', '2026-05-24 09:43:48'),
(23, 19, '2026-05-12', '18:00:00', '19:00:00', 'HUY', 'Khách bị ốm', '2026-05-24 14:00:37'),
(24, 19, '2026-05-12', '19:30:00', '21:00:00', 'HOAN_THANH', 'Đã hoàn thành buổi tập.', '2026-05-24 14:06:25'),
(25, 19, '2026-05-12', '18:00:00', '19:00:00', 'HOAN_THANH', 'Đã hoàn thành buổi tập.', '2026-05-24 16:24:42'),
(26, 20, '2026-05-16', '07:00:00', '09:00:00', 'HOAN_THANH', 'Đã hoàn thành buổi tập đầu tiên.', '2026-05-26 00:11:06'),
(27, 21, '2026-03-06', '18:00:00', '19:30:00', 'HOAN_THANH', 'Đã hoàn thành buổi PT đầu tiên.', '2026-05-31 09:38:42'),
(28, 21, '2026-03-13', '18:00:00', '19:30:00', 'HOAN_THANH', 'Đã hoàn thành buổi PT thứ hai.', '2026-05-31 09:38:42'),
(29, 21, '2026-03-20', '18:00:00', '19:30:00', 'HOAN_THANH', 'Đã hoàn thành buổi PT thứ ba.', '2026-05-31 09:38:42'),
(30, 21, '2026-05-31', '15:00:00', '17:00:00', 'DA_LEN_LICH', '', '2026-05-31 13:57:34'),
(31, 20, '2026-05-31', '15:00:00', '17:00:00', 'DA_LEN_LICH', '', '2026-05-31 13:58:48');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `nhatkybuoitap`
--

DROP TABLE IF EXISTS `nhatkybuoitap`;
CREATE TABLE `nhatkybuoitap` (
  `ma_nhat_ky` int(11) NOT NULL,
  `ma_lich_tap` int(11) NOT NULL,
  `muc_tieu_buoi_tap` varchar(100) DEFAULT NULL,
  `nhom_co_chinh` varchar(100) DEFAULT NULL,
  `thoi_luong_phut` int(11) DEFAULT NULL,
  `muc_do_hoan_thanh` varchar(30) DEFAULT NULL,
  `tinh_trang_hoi_vien` varchar(100) DEFAULT NULL,
  `nhan_xet_pt` text DEFAULT NULL,
  `ke_hoach_buoi_sau` text DEFAULT NULL,
  `ma_tai_khoan_tao` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT NULL ON UPDATE current_timestamp()
) ;

--
-- Đang đổ dữ liệu cho bảng `nhatkybuoitap`
--

INSERT INTO `nhatkybuoitap` (`ma_nhat_ky`, `ma_lich_tap`, `muc_tieu_buoi_tap`, `nhom_co_chinh`, `thoi_luong_phut`, `muc_do_hoan_thanh`, `tinh_trang_hoi_vien`, `nhan_xet_pt`, `ke_hoach_buoi_sau`, `ma_tai_khoan_tao`, `created_at`, `updated_at`) VALUES
(1, 16, 'Tăng cân', 'Ngực vai tay sau', 60, 'TOT', NULL, 'Hoàn thành buổi tập ngắn, tập trung sửa kỹ thuật cơ bản.', 'Buổi sau tiếp tục sửa kỹ thuật và tăng thời lượng tập.', 3, '2026-05-16 22:43:48', '2026-05-29 17:12:54'),
(2, 19, 'Tăng cân', 'Ngực Vai', 120, 'TOT', NULL, 'Hoàn thành buổi tập đúng kế hoạch, cần cải thiện nhịp thở ở các bài nặng.', 'Buổi sau tập trung kỹ thuật kéo và kiểm soát form.', 1, '2026-05-24 09:12:20', '2026-05-29 17:12:54'),
(4, 18, NULL, NULL, 90, NULL, NULL, 'Hoàn thành buổi tập, hội viên phối hợp tốt nhưng cần tăng độ ổn định kỹ thuật.', 'Buổi sau duy trì cường độ vừa, ưu tiên kỹ thuật trước khi tăng tải.', 1, '2026-05-24 09:17:27', '2026-05-29 17:12:54'),
(5, 15, 'Tăng cân', 'Ngực Vai', 90, NULL, NULL, 'Hoàn thành buổi tập, cường độ phù hợp với thể trạng hiện tại.', 'Buổi sau tập trung thân dưới và kiểm soát biên độ động tác.', 1, '2026-05-24 09:28:02', '2026-05-29 17:12:54'),
(6, 21, NULL, NULL, 100, NULL, NULL, 'Hoàn thành đầy đủ nội dung buổi tập, kỹ thuật ổn định.', 'Buổi sau tăng nhẹ cường độ và bổ sung bài core.', 1, '2026-05-24 16:10:10', '2026-05-29 17:12:54'),
(7, 23, NULL, NULL, NULL, NULL, NULL, 'Hội viên báo không đảm bảo sức khỏe nên hủy buổi tập.', 'Sắp xếp lại buổi tập khi hội viên ổn định sức khỏe.', 1, '2026-05-24 16:11:16', '2026-05-29 17:12:54'),
(8, 22, NULL, NULL, NULL, NULL, NULL, 'Hội viên báo ốm trước giờ tập, buổi tập được hủy theo yêu cầu.', 'Liên hệ hội viên để sắp xếp lại lịch trong tuần tới.', 1, '2026-05-24 16:18:56', '2026-05-29 17:12:54'),
(9, 20, NULL, NULL, 95, NULL, NULL, 'Hoàn thành buổi tập, thể lực tốt và kiểm soát động tác khá.', 'Buổi sau tiếp tục nhóm cơ thân trên, chú ý kiểm soát nhịp thở.', 6, '2026-05-25 15:41:24', '2026-05-29 17:12:54'),
(10, 17, NULL, NULL, NULL, NULL, NULL, 'Hội viên bận đột xuất, đã báo hủy trước giờ tập.', 'Chủ động đặt lại lịch phù hợp với thời gian của hội viên.', 6, '2026-05-25 15:41:58', '2026-05-29 17:12:54');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `phancongpt`
--

DROP TABLE IF EXISTS `phancongpt`;
CREATE TABLE `phancongpt` (
  `ma_phan_cong` int(11) NOT NULL,
  `ma_dang_ky` int(11) NOT NULL,
  `ma_pt` int(11) NOT NULL,
  `ngay_phan_cong` date NOT NULL DEFAULT curdate(),
  `ngay_ket_thuc` date DEFAULT NULL,
  `trang_thai` varchar(30) NOT NULL DEFAULT 'DANG_PHU_TRACH',
  `ghi_chu` varchar(255) DEFAULT NULL
) ;

--
-- Đang đổ dữ liệu cho bảng `phancongpt`
--

INSERT INTO `phancongpt` (`ma_phan_cong`, `ma_dang_ky`, `ma_pt`, `ngay_phan_cong`, `ngay_ket_thuc`, `trang_thai`, `ghi_chu`) VALUES
(1, 2, 1, '2026-03-01', '2026-03-11', 'DA_KET_THUC', 'Phân công PT Minh cho gói PT 24 buổi của Bùi Đức Anh'),
(2, 2, 1, '2026-03-12', NULL, 'DANG_PHU_TRACH', ''),
(3, 6, 1, '2026-04-03', NULL, 'DANG_PHU_TRACH', ''),
(4, 7, 1, '2026-04-01', NULL, 'DANG_PHU_TRACH', ''),
(5, 17, 2, '2026-04-12', '2026-04-14', 'DA_KET_THUC', 'Buổi 1'),
(6, 18, 2, '2026-04-15', '2026-04-15', 'DA_KET_THUC', ''),
(7, 18, 1, '2026-04-15', '2026-04-16', 'DA_KET_THUC', ''),
(8, 17, 5, '2026-04-14', NULL, 'DANG_PHU_TRACH', 'PT mới thay cho PT Lan nghỉ'),
(9, 18, 5, '2026-04-16', NULL, 'DANG_PHU_TRACH', 'Buổi đầu tập với PT'),
(10, 25, 5, '2026-04-21', NULL, 'DANG_PHU_TRACH', ''),
(11, 30, 5, '2026-05-08', '2026-05-08', 'DA_KET_THUC', ''),
(12, 30, 5, '2026-05-08', '2026-05-08', 'DA_KET_THUC', ''),
(13, 30, 1, '2026-05-08', '2026-05-10', 'DA_KET_THUC', ''),
(14, 30, 5, '2026-05-10', NULL, 'DANG_PHU_TRACH', ''),
(15, 33, 6, '2026-05-10', '2026-05-11', 'DA_KET_THUC', ''),
(16, 13, 6, '2026-04-18', NULL, 'DANG_PHU_TRACH', ''),
(17, 33, 5, '2026-05-11', NULL, 'DANG_PHU_TRACH', 'Tập buổi 1 - Push day'),
(18, 34, 1, '2026-05-02', NULL, 'DANG_PHU_TRACH', ''),
(19, 35, 6, '2026-05-12', NULL, 'DANG_PHU_TRACH', ''),
(20, 37, 7, '2026-05-16', NULL, 'DANG_PHU_TRACH', ''),
(21, 28, 6, '2026-03-02', NULL, 'DANG_PHU_TRACH', 'Phân công PT Hà Thế Anh cho gói PT 24 buổi của Trần Quốc Đạt.');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `pt`
--

DROP TABLE IF EXISTS `pt`;
CREATE TABLE `pt` (
  `ma_pt` int(11) NOT NULL,
  `ma_tai_khoan` int(11) DEFAULT NULL,
  `ho_ten` varchar(100) NOT NULL,
  `so_dien_thoai` varchar(15) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `chuyen_mon` varchar(100) DEFAULT NULL,
  `kinh_nghiem` varchar(100) DEFAULT NULL,
  `trang_thai_lam_viec` varchar(30) NOT NULL DEFAULT 'DANG_LAM_VIEC',
  `ghi_chu` varchar(255) DEFAULT NULL
) ;

--
-- Đang đổ dữ liệu cho bảng `pt`
--

INSERT INTO `pt` (`ma_pt`, `ma_tai_khoan`, `ho_ten`, `so_dien_thoai`, `email`, `chuyen_mon`, `kinh_nghiem`, `trang_thai_lam_viec`, `ghi_chu`) VALUES
(1, 3, 'Nguyễn Văn Minh', '0906247185', 'minh.nv@progym.vn', 'Tăng cơ - giảm mỡ', '3 năm', 'DANG_LAM_VIEC', 'PT phụ trách nhóm hội viên nam'),
(2, 4, 'Trần Thị Lan', '0971385264', 'lan.tt@progym.vn', 'Giảm mỡ - body shaping', '4', 'NGUNG_LAM_VIEC', 'PT phụ trách nhóm hội viên nữ'),
(5, 6, 'Nguyễn Mạnh Hà', '0962718453', 'ha.nm@progym.vn', 'Kick boxing, Muay Thai', '5', 'DANG_LAM_VIEC', NULL),
(6, 7, 'Hà Thế Anh', '0982178100', 'theanh.ha@progym.vn', 'Tăng cơ - giảm mỡ', '5', 'DANG_LAM_VIEC', NULL),
(7, 8, 'Nguyễn Văn Huy', '0381919301', 'nvanhuy@gmail.com', 'Tăng cơ - giảm mỡ', '5', 'DANG_LAM_VIEC', NULL),
(8, NULL, 'Vũ Minh Hoàng', '0381929103', 'minhoang01@gmail.com', 'Tăng cơ giảm mỡ', '4 năm', 'TAM_NGHI', NULL);

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `taikhoan`
--

DROP TABLE IF EXISTS `taikhoan`;
CREATE TABLE `taikhoan` (
  `ma_tai_khoan` int(11) NOT NULL,
  `ten_dang_nhap` varchar(50) NOT NULL,
  `mat_khau` varchar(255) NOT NULL,
  `ho_ten` varchar(100) NOT NULL,
  `so_dien_thoai` varchar(15) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `trang_thai` varchar(30) NOT NULL DEFAULT 'HOAT_DONG',
  `ma_vai_tro` int(11) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `lan_dang_nhap_cuoi` datetime DEFAULT NULL
) ;

--
-- Đang đổ dữ liệu cho bảng `taikhoan`
--

INSERT INTO `taikhoan` (`ma_tai_khoan`, `ten_dang_nhap`, `mat_khau`, `ho_ten`, `so_dien_thoai`, `email`, `trang_thai`, `ma_vai_tro`, `created_at`, `lan_dang_nhap_cuoi`) VALUES
(1, 'admin', 'Admin@2026', 'Hoàng Minh Đức', '0914862375', 'duc.hm@progym.vn', 'HOAT_DONG', 1, '2026-05-10 22:25:38', '2026-06-01 15:36:50'),
(2, 'letan', 'Letan@2026', 'Đỗ Thi Hồng', '0983517426', 'hong.dt@progym.vn', 'HOAT_DONG', 2, '2026-05-10 22:25:38', '2026-05-31 20:05:29'),
(3, 'ptminh', '123456', 'Nguyễn Văn Minh', '0906247185', 'minh.nv@progym.vn', 'HOAT_DONG', 3, '2026-05-10 22:25:38', NULL),
(4, 'ptlan', '123456', 'Trần Thị Lan', '0971385264', 'lan.tt@progym.vn', 'TAM_KHOA', 3, '2026-05-10 22:25:38', NULL),
(5, 'letan02', '654321', 'Trịnh Thi Tâm', '0928312890', 'tam.tt@progym.vn', 'HOAT_DONG', 2, '2026-05-15 09:54:22', NULL),
(6, 'ptha', '123456', 'Nguyễn Mạnh Hà', '0962718453', 'ha.nm@progym.vn', 'HOAT_DONG', 3, '2026-05-15 09:57:33', '2026-05-31 20:54:02'),
(7, 'pttheanh', '123456', 'Hà Thế Anh', '0982178100', 'theanh.ha@progym.vn', 'HOAT_DONG', 3, '2026-05-25 15:11:32', NULL),
(8, 'pthuy', '123456', 'Nguyễn Văn Huy', '0381919301', 'pthuy@progym.vn', 'HOAT_DONG', 3, '2026-05-25 15:17:58', NULL),
(9, 'lequynh', '123456', 'Lê Phương Quỳnh', '0894621375', 'quynh.lp@progym.vn', 'TAM_KHOA', 2, '2026-05-25 15:23:09', NULL),
(10, 'letan03', '123456', 'Nguyễn Thị Thu', '0391012190', 'letan03@progym.vn', 'TAM_KHOA', 2, '2026-05-25 17:55:11', NULL);

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `thanhtoan`
--

DROP TABLE IF EXISTS `thanhtoan`;
CREATE TABLE `thanhtoan` (
  `ma_thanh_toan` int(11) NOT NULL,
  `ma_dang_ky` int(11) NOT NULL,
  `ma_tai_khoan_tao` int(11) DEFAULT NULL,
  `ngay_thanh_toan` datetime NOT NULL DEFAULT current_timestamp(),
  `so_tien` decimal(12,2) NOT NULL,
  `hinh_thuc_thanh_toan` varchar(50) NOT NULL,
  `trang_thai_thanh_toan` varchar(30) NOT NULL DEFAULT 'DA_THANH_TOAN',
  `ghi_chu` varchar(255) DEFAULT NULL
) ;

--
-- Đang đổ dữ liệu cho bảng `thanhtoan`
--

INSERT INTO `thanhtoan` (`ma_thanh_toan`, `ma_dang_ky`, `ma_tai_khoan_tao`, `ngay_thanh_toan`, `so_tien`, `hinh_thuc_thanh_toan`, `trang_thai_thanh_toan`, `ghi_chu`) VALUES
(1, 1, 2, '2026-03-15 08:31:00', 1350000.00, 'CHUYEN_KHOAN', 'DA_THANH_TOAN', 'Thanh toán đủ gói tập tự do 3 tháng'),
(2, 2, 2, '2026-03-01 08:32:00', 5500000.00, 'CHUYEN_KHOAN', 'DA_THANH_TOAN', 'Thanh toán đủ gói PT 12 buổi'),
(3, 3, 2, '2026-05-05 08:33:00', 500000.00, 'TIEN_MAT', 'DA_THANH_TOAN', 'Thanh toán đủ gói tập tự do 1 tháng'),
(4, 4, 1, '2026-03-03 08:34:00', 1350000.00, 'TIEN_MAT', 'DA_THANH_TOAN', 'Thanh toán đủ gói tập tự do 3 tháng'),
(5, 5, 1, '2026-03-25 08:35:00', 1350000.00, 'CHUYEN_KHOAN', 'DA_THANH_TOAN', 'Thanh toán khi tạo mới hội viên và đăng ký gói'),
(6, 6, 1, '2026-04-02 08:36:00', 3000000.00, 'CHUYEN_KHOAN', 'DA_THANH_TOAN', 'Thanh toán khi đăng ký thêm gói cho hội viên cũ'),
(7, 7, 1, '2026-04-01 08:37:00', 3000000.00, 'TIEN_MAT', 'DA_THANH_TOAN', 'Thanh toán khi tạo mới hội viên và đăng ký gói'),
(8, 8, 1, '2026-03-15 08:38:00', 1350000.00, 'TIEN_MAT', 'DA_THANH_TOAN', 'Thanh toán khi tạo mới hội viên và đăng ký gói'),
(9, 9, 1, '2026-03-20 08:39:00', 1350000.00, 'CHUYEN_KHOAN', 'DA_THANH_TOAN', 'Thanh toán khi tạo mới hội viên và đăng ký gói'),
(10, 11, 1, '2026-05-11 10:00:00', 1000000.00, 'TIEN_MAT', 'DA_THANH_TOAN', 'Thanh toán khi tạo mới hội viên và đăng ký gói'),
(11, 11, 1, '2026-05-11 10:25:00', 350000.00, 'TIEN_MAT', 'DA_THANH_TOAN', ''),
(12, 12, 1, '2026-04-05 08:42:00', 3000000.00, 'CHUYEN_KHOAN', 'DA_THANH_TOAN', 'Thanh toán khi tạo mới hội viên và đăng ký gói'),
(13, 14, 1, '2026-04-10 08:43:00', 3000000.00, 'CHUYEN_KHOAN', 'DA_THANH_TOAN', 'Thanh toán khi tạo mới hội viên và đăng ký gói'),
(14, 15, 1, '2026-04-12 08:44:00', 3000000.00, 'TIEN_MAT', 'DA_THANH_TOAN', 'Thanh toán khi đăng ký thêm gói cho hội viên cũ'),
(15, 10, 1, '2026-03-25 08:45:00', 1350000.00, 'TIEN_MAT', 'DA_THANH_TOAN', ''),
(16, 13, 1, '2026-04-10 08:46:00', 3000000.00, 'TIEN_MAT', 'DA_THANH_TOAN', ''),
(17, 16, 1, '2026-03-10 08:47:00', 1350000.00, 'TIEN_MAT', 'DA_THANH_TOAN', 'Bổ sung giao dịch thanh toán do lỗi khi tạo hội viên'),
(18, 17, 1, '2026-04-12 08:48:00', 3000000.00, 'TIEN_MAT', 'DA_THANH_TOAN', 'Thanh toán khi tạo mới hội viên và đăng ký gói'),
(19, 18, 1, '2026-04-15 08:49:00', 2000000.00, 'TIEN_MAT', 'DA_THANH_TOAN', 'Thanh toán khi tạo mới hội viên và đăng ký gói'),
(20, 18, 1, '2026-04-15 08:50:00', 1000000.00, 'TIEN_MAT', 'DA_THANH_TOAN', ''),
(21, 19, 1, '2026-05-10 08:51:00', 500000.00, 'CHUYEN_KHOAN', 'DA_THANH_TOAN', 'Thanh toán khi tạo mới hội viên và đăng ký gói'),
(22, 20, 1, '2026-04-13 08:52:00', 500000.00, 'CHUYEN_KHOAN', 'DA_THANH_TOAN', 'Thanh toán khi tạo mới hội viên và đăng ký gói'),
(23, 21, 1, '2026-03-15 08:53:00', 1350000.00, 'CHUYEN_KHOAN', 'DA_THANH_TOAN', 'Thanh toán khi tạo mới hội viên và đăng ký gói'),
(24, 22, 1, '2026-03-20 08:54:00', 1350000.00, 'CHUYEN_KHOAN', 'DA_THANH_TOAN', 'Thanh toán khi tạo mới hội viên và đăng ký gói'),
(25, 23, 1, '2026-03-14 08:55:00', 3000000.00, 'CHUYEN_KHOAN', 'DA_THANH_TOAN', 'Thanh toán khi đăng ký thêm gói cho hội viên cũ'),
(26, 24, 1, '2026-04-01 08:56:00', 1350000.00, 'TIEN_MAT', 'DA_THANH_TOAN', 'Thanh toán khi tạo mới hội viên và đăng ký gói'),
(27, 25, 1, '2026-04-20 08:57:00', 2000000.00, 'TIEN_MAT', 'DA_THANH_TOAN', 'Thanh toán khi đăng ký thêm gói cho hội viên cũ'),
(28, 26, 1, '2026-05-03 08:58:00', 500000.00, 'CHUYEN_KHOAN', 'DA_THANH_TOAN', 'Thanh toán khi tạo mới hội viên và đăng ký gói'),
(29, 25, 1, '2026-04-20 08:59:00', 1000000.00, 'TIEN_MAT', 'DA_THANH_TOAN', ''),
(30, 27, 1, '2026-03-08 09:00:00', 1000000.00, 'CHUYEN_KHOAN', 'DA_THANH_TOAN', 'Thanh toán khi tạo mới hội viên và đăng ký gói'),
(31, 27, 1, '2026-03-08 09:01:00', 300000.00, 'TIEN_MAT', 'DA_THANH_TOAN', ''),
(32, 27, 1, '2026-03-08 09:02:00', 50000.00, 'TIEN_MAT', 'DA_THANH_TOAN', ''),
(33, 28, 1, '2026-03-01 09:03:00', 5500000.00, 'CHUYEN_KHOAN', 'DA_THANH_TOAN', 'Thanh toán khi tạo mới hội viên và đăng ký gói'),
(34, 29, 1, '2026-05-01 09:04:00', 500000.00, 'TIEN_MAT', 'DA_THANH_TOAN', 'Thanh toán khi tạo mới hội viên và đăng ký gói'),
(37, 30, 1, '2026-05-08 09:07:00', 3000000.00, 'TIEN_MAT', 'DA_THANH_TOAN', 'Thanh toán khi đăng ký thêm gói cho hội viên cũ'),
(38, 31, 1, '2026-04-10 09:08:00', 100000.00, 'TIEN_MAT', 'DA_THANH_TOAN', 'Thanh toán khi tạo mới hội viên và đăng ký gói'),
(39, 32, 1, '2026-05-05 09:09:00', 500000.00, 'CHUYEN_KHOAN', 'DA_THANH_TOAN', 'Thanh toán khi tạo mới hội viên và đăng ký gói'),
(40, 33, 1, '2026-05-10 09:10:00', 3000000.00, 'TIEN_MAT', 'DA_THANH_TOAN', 'Thanh toán khi đăng ký thêm gói cho hội viên cũ'),
(41, 34, 1, '2026-05-01 09:11:00', 3000000.00, 'TIEN_MAT', 'DA_THANH_TOAN', 'Thanh toán khi tạo mới hội viên và đăng ký gói'),
(42, 35, 1, '2026-05-12 09:12:00', 5500000.00, 'TIEN_MAT', 'DA_THANH_TOAN', 'Thanh toán khi tạo mới hội viên và đăng ký gói'),
(43, 36, 2, '2026-05-05 09:13:00', 500000.00, 'CHUYEN_KHOAN', 'DA_THANH_TOAN', 'Thanh toán khi tạo mới hội viên và đăng ký gói'),
(44, 37, 2, '2026-05-16 09:14:00', 3000000.00, 'CHUYEN_KHOAN', 'DA_THANH_TOAN', 'Thanh toán khi đăng ký thêm gói cho hội viên cũ'),
(45, 38, 2, '2026-05-06 09:15:00', 500000.00, 'TIEN_MAT', 'DA_THANH_TOAN', 'Thanh toán khi đăng ký thêm gói cho hội viên cũ'),
(46, 39, 2, '2026-05-07 09:16:00', 500000.00, 'CHUYEN_KHOAN', 'DA_THANH_TOAN', 'Thanh toán khi tạo mới hội viên và đăng ký gói'),
(48, 40, 1, '2026-03-25 09:18:00', 1000000.00, 'CHUYEN_KHOAN', 'DA_THANH_TOAN', 'Thanh toán khi tạo mới hội viên và đăng ký gói'),
(49, 40, 1, '2026-03-25 09:19:00', 350000.00, 'TIEN_MAT', 'DA_THANH_TOAN', ''),
(50, 41, 1, '2026-05-31 13:36:24', 500000.00, 'CHUYEN_KHOAN', 'DA_THANH_TOAN', 'Thanh toán khi đăng ký thêm gói cho hội viên cũ');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `trangthietbi`
--

DROP TABLE IF EXISTS `trangthietbi`;
CREATE TABLE `trangthietbi` (
  `ma_thiet_bi` int(11) NOT NULL,
  `ten_thiet_bi` varchar(100) NOT NULL,
  `loai_thiet_bi` varchar(100) NOT NULL,
  `vi_tri` varchar(100) DEFAULT NULL,
  `ngay_mua` date DEFAULT NULL,
  `tinh_trang` varchar(50) NOT NULL DEFAULT 'TOT',
  `ghi_chu` varchar(255) DEFAULT NULL,
  `hinh_anh` varchar(255) DEFAULT NULL
) ;

--
-- Đang đổ dữ liệu cho bảng `trangthietbi`
--

INSERT INTO `trangthietbi` (`ma_thiet_bi`, `ten_thiet_bi`, `loai_thiet_bi`, `vi_tri`, `ngay_mua`, `tinh_trang`, `ghi_chu`, `hinh_anh`) VALUES
(1, 'Máy chạy bộ 01', 'Cardio', 'Khu cardio tầng 1', '2025-01-10', 'TOT', 'Hoạt động ổn định, kiểm tra định kỳ hàng tháng.', 'uploads/equipment/4f5944e4d0d5415599e4aecb245afc50.webp'),
(2, 'Ghế đẩy ngực 01', 'Máy tập sức mạnh', 'Khu tập ngực', '2025-02-15', 'NGUNG_SU_DUNG', 'Bỏ ghế tập kiểu này', 'uploads/equipment/a4c0121455104f8a9e33cf09eb4e3521.webp'),
(3, 'Máy kéo xô 01', 'Máy tập sức mạnh', 'Khu tập lưng', '2025-03-20', 'TOT', 'Đã tra dầu và kiểm tra cáp kéo, vận hành ổn định.', 'uploads/equipment/657c66d52cf6493690cc16b4b65eca2b.webp'),
(4, 'Bộ tạ tay 5kg - 30kg', 'Tạ tự do', 'Khu tạ tự do', '2026-05-13', 'TOT', 'Bộ tạ đầy đủ, sắp xếp tại khu tạ tự do.', 'uploads/equipment/733bb76f2a854e729600ad358a17d024.jpg'),
(5, 'Leg Extension Machine', 'Máy tập sức mạnh', 'Khu tập chân', '2026-05-24', 'TOT', 'Thiết bị mới, hoạt động ổn định.', 'uploads/equipment/a6379484a96945578f18b5037862ac0d.png'),
(6, 'Máy đạp xe cardio 01', 'Cardio', 'Khu cardio tầng 1', '2025-01-18', 'DANG_BAO_TRI', 'Hoạt động ổn định, dùng cho bài tập tim mạch cường độ vừa.', NULL),
(7, 'Smith Machine 01', 'Máy tập sức mạnh', 'Khu tạ tự do', '2025-02-05', 'TOT', 'Khung máy ổn định, dùng cho squat và đẩy ngực có hỗ trợ ray dẫn.', NULL),
(8, 'Squat Rack 01', 'Máy tập sức mạnh', 'Khu tạ tự do', '2025-02-20', 'TOT', 'Khung squat chắc chắn, đã kiểm tra chốt an toàn.', NULL),
(9, 'Chest Press Machine 01', 'Máy tập sức mạnh', 'Khu tập ngực', '2025-03-05', 'TOT', 'Máy ép ngực hoạt động ổn định, tay cầm và đệm ghế còn tốt.', NULL),
(10, 'Cable Crossover 01', 'Máy tập sức mạnh', 'Khu tập lưng - vai', '2025-03-18', 'TOT', 'Cáp kéo vận hành ổn định, phù hợp nhiều bài tập thân trên.', NULL),
(11, 'Leg Press Machine 01', 'Máy tập sức mạnh', 'Khu tập chân', '2025-04-02', 'TOT', 'Máy đạp đùi hoạt động ổn định, ray trượt đã được kiểm tra.', NULL),
(12, 'Ghế tập điều chỉnh 01', 'Ghế tập', 'Khu tạ tự do', '2025-04-16', 'TOT', 'Ghế điều chỉnh được nhiều góc, bọc ghế còn tốt.', NULL),
(13, 'Thanh đòn Olympic và bánh tạ', 'Tạ tự do', 'Khu tạ tự do', '2025-05-05', 'DANG_BAO_TRI', NULL, NULL),
(14, 'Pec Fly Rear Delt', 'Strength', 'Khu tập ngực', '2026-05-31', 'TOT', NULL, 'uploads/equipment/695fcbe360e44afb98b1e3d726df713c.png');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `vaitro`
--

DROP TABLE IF EXISTS `vaitro`;
CREATE TABLE `vaitro` (
  `ma_vai_tro` int(11) NOT NULL,
  `ten_vai_tro` varchar(50) NOT NULL,
  `mo_ta` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Đang đổ dữ liệu cho bảng `vaitro`
--

INSERT INTO `vaitro` (`ma_vai_tro`, `ten_vai_tro`, `mo_ta`) VALUES
(1, 'ADMIN', 'Quản trị hệ thống và theo dõi toàn bộ hoạt động trung tâm'),
(2, 'LE_TAN', 'Tiếp nhận hội viên, đăng ký gói, thanh toán, check-in/check-out'),
(3, 'PT', 'Huấn luyện viên cá nhân, xem lịch tập và cập nhật trạng thái buổi tập');

--
-- Chỉ mục cho các bảng đã đổ
--

--
-- Chỉ mục cho bảng `baotrithietbi`
--
ALTER TABLE `baotrithietbi`
  ADD PRIMARY KEY (`ma_bao_tri`),
  ADD KEY `fk_baotri_thietbi` (`ma_thiet_bi`);

--
-- Chỉ mục cho bảng `checkinout`
--
ALTER TABLE `checkinout`
  ADD PRIMARY KEY (`ma_check`),
  ADD KEY `fk_check_lichtap` (`ma_lich_tap`),
  ADD KEY `idx_check_hoivien` (`ma_hoi_vien`),
  ADD KEY `idx_check_dangky` (`ma_dang_ky`);

--
-- Chỉ mục cho bảng `chitietbaitap`
--
ALTER TABLE `chitietbaitap`
  ADD PRIMARY KEY (`ma_chi_tiet`),
  ADD KEY `fk_chitiet_nhatky` (`ma_nhat_ky`);

--
-- Chỉ mục cho bảng `dangkygoitap`
--
ALTER TABLE `dangkygoitap`
  ADD PRIMARY KEY (`ma_dang_ky`),
  ADD KEY `fk_dangky_goitap` (`ma_goi_tap`),
  ADD KEY `idx_dangky_hoivien` (`ma_hoi_vien`);

--
-- Chỉ mục cho bảng `goitap`
--
ALTER TABLE `goitap`
  ADD PRIMARY KEY (`ma_goi_tap`);

--
-- Chỉ mục cho bảng `hoivien`
--
ALTER TABLE `hoivien`
  ADD PRIMARY KEY (`ma_hoi_vien`),
  ADD UNIQUE KEY `so_dien_thoai` (`so_dien_thoai`),
  ADD KEY `idx_hoivien_ho_ten` (`ho_ten`);

--
-- Chỉ mục cho bảng `lichtap`
--
ALTER TABLE `lichtap`
  ADD PRIMARY KEY (`ma_lich_tap`),
  ADD KEY `fk_lichtap_phancong` (`ma_phan_cong`),
  ADD KEY `idx_lichtap_ngay_gio` (`ngay_tap`,`gio_bat_dau`,`gio_ket_thuc`);

--
-- Chỉ mục cho bảng `nhatkybuoitap`
--
ALTER TABLE `nhatkybuoitap`
  ADD PRIMARY KEY (`ma_nhat_ky`),
  ADD UNIQUE KEY `uq_nhatky_lichtap` (`ma_lich_tap`),
  ADD KEY `fk_nhatky_taikhoan` (`ma_tai_khoan_tao`);

--
-- Chỉ mục cho bảng `phancongpt`
--
ALTER TABLE `phancongpt`
  ADD PRIMARY KEY (`ma_phan_cong`),
  ADD KEY `fk_phancong_pt` (`ma_pt`),
  ADD KEY `idx_phancong_dangky` (`ma_dang_ky`);

--
-- Chỉ mục cho bảng `pt`
--
ALTER TABLE `pt`
  ADD PRIMARY KEY (`ma_pt`),
  ADD UNIQUE KEY `so_dien_thoai` (`so_dien_thoai`),
  ADD KEY `fk_pt_taikhoan` (`ma_tai_khoan`),
  ADD KEY `idx_pt_ho_ten` (`ho_ten`);

--
-- Chỉ mục cho bảng `taikhoan`
--
ALTER TABLE `taikhoan`
  ADD PRIMARY KEY (`ma_tai_khoan`),
  ADD UNIQUE KEY `ten_dang_nhap` (`ten_dang_nhap`),
  ADD KEY `fk_taikhoan_vaitro` (`ma_vai_tro`);

--
-- Chỉ mục cho bảng `thanhtoan`
--
ALTER TABLE `thanhtoan`
  ADD PRIMARY KEY (`ma_thanh_toan`),
  ADD KEY `fk_thanhtoan_taikhoan` (`ma_tai_khoan_tao`),
  ADD KEY `idx_thanhtoan_dangky` (`ma_dang_ky`);

--
-- Chỉ mục cho bảng `trangthietbi`
--
ALTER TABLE `trangthietbi`
  ADD PRIMARY KEY (`ma_thiet_bi`);

--
-- Chỉ mục cho bảng `vaitro`
--
ALTER TABLE `vaitro`
  ADD PRIMARY KEY (`ma_vai_tro`),
  ADD UNIQUE KEY `ten_vai_tro` (`ten_vai_tro`);

--
-- AUTO_INCREMENT cho các bảng đã đổ
--

--
-- AUTO_INCREMENT cho bảng `baotrithietbi`
--
ALTER TABLE `baotrithietbi`
  MODIFY `ma_bao_tri` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT cho bảng `checkinout`
--
ALTER TABLE `checkinout`
  MODIFY `ma_check` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT cho bảng `chitietbaitap`
--
ALTER TABLE `chitietbaitap`
  MODIFY `ma_chi_tiet` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT cho bảng `dangkygoitap`
--
ALTER TABLE `dangkygoitap`
  MODIFY `ma_dang_ky` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT cho bảng `goitap`
--
ALTER TABLE `goitap`
  MODIFY `ma_goi_tap` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT cho bảng `hoivien`
--
ALTER TABLE `hoivien`
  MODIFY `ma_hoi_vien` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT cho bảng `lichtap`
--
ALTER TABLE `lichtap`
  MODIFY `ma_lich_tap` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT cho bảng `nhatkybuoitap`
--
ALTER TABLE `nhatkybuoitap`
  MODIFY `ma_nhat_ky` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT cho bảng `phancongpt`
--
ALTER TABLE `phancongpt`
  MODIFY `ma_phan_cong` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT cho bảng `pt`
--
ALTER TABLE `pt`
  MODIFY `ma_pt` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT cho bảng `taikhoan`
--
ALTER TABLE `taikhoan`
  MODIFY `ma_tai_khoan` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT cho bảng `thanhtoan`
--
ALTER TABLE `thanhtoan`
  MODIFY `ma_thanh_toan` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT cho bảng `trangthietbi`
--
ALTER TABLE `trangthietbi`
  MODIFY `ma_thiet_bi` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT cho bảng `vaitro`
--
ALTER TABLE `vaitro`
  MODIFY `ma_vai_tro` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Các ràng buộc cho các bảng đã đổ
--

--
-- Các ràng buộc cho bảng `baotrithietbi`
--
ALTER TABLE `baotrithietbi`
  ADD CONSTRAINT `fk_baotri_thietbi` FOREIGN KEY (`ma_thiet_bi`) REFERENCES `trangthietbi` (`ma_thiet_bi`) ON UPDATE CASCADE;

--
-- Các ràng buộc cho bảng `checkinout`
--
ALTER TABLE `checkinout`
  ADD CONSTRAINT `fk_check_dangky` FOREIGN KEY (`ma_dang_ky`) REFERENCES `dangkygoitap` (`ma_dang_ky`) ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_check_hoivien` FOREIGN KEY (`ma_hoi_vien`) REFERENCES `hoivien` (`ma_hoi_vien`) ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_check_lichtap` FOREIGN KEY (`ma_lich_tap`) REFERENCES `lichtap` (`ma_lich_tap`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Các ràng buộc cho bảng `chitietbaitap`
--
ALTER TABLE `chitietbaitap`
  ADD CONSTRAINT `fk_chitiet_nhatky` FOREIGN KEY (`ma_nhat_ky`) REFERENCES `nhatkybuoitap` (`ma_nhat_ky`) ON DELETE CASCADE;

--
-- Các ràng buộc cho bảng `dangkygoitap`
--
ALTER TABLE `dangkygoitap`
  ADD CONSTRAINT `fk_dangky_goitap` FOREIGN KEY (`ma_goi_tap`) REFERENCES `goitap` (`ma_goi_tap`) ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_dangky_hoivien` FOREIGN KEY (`ma_hoi_vien`) REFERENCES `hoivien` (`ma_hoi_vien`) ON UPDATE CASCADE;

--
-- Các ràng buộc cho bảng `lichtap`
--
ALTER TABLE `lichtap`
  ADD CONSTRAINT `fk_lichtap_phancong` FOREIGN KEY (`ma_phan_cong`) REFERENCES `phancongpt` (`ma_phan_cong`) ON UPDATE CASCADE;

--
-- Các ràng buộc cho bảng `nhatkybuoitap`
--
ALTER TABLE `nhatkybuoitap`
  ADD CONSTRAINT `fk_nhatky_lichtap` FOREIGN KEY (`ma_lich_tap`) REFERENCES `lichtap` (`ma_lich_tap`),
  ADD CONSTRAINT `fk_nhatky_taikhoan` FOREIGN KEY (`ma_tai_khoan_tao`) REFERENCES `taikhoan` (`ma_tai_khoan`);

--
-- Các ràng buộc cho bảng `phancongpt`
--
ALTER TABLE `phancongpt`
  ADD CONSTRAINT `fk_phancong_dangky` FOREIGN KEY (`ma_dang_ky`) REFERENCES `dangkygoitap` (`ma_dang_ky`) ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_phancong_pt` FOREIGN KEY (`ma_pt`) REFERENCES `pt` (`ma_pt`) ON UPDATE CASCADE;

--
-- Các ràng buộc cho bảng `pt`
--
ALTER TABLE `pt`
  ADD CONSTRAINT `fk_pt_taikhoan` FOREIGN KEY (`ma_tai_khoan`) REFERENCES `taikhoan` (`ma_tai_khoan`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Các ràng buộc cho bảng `taikhoan`
--
ALTER TABLE `taikhoan`
  ADD CONSTRAINT `fk_taikhoan_vaitro` FOREIGN KEY (`ma_vai_tro`) REFERENCES `vaitro` (`ma_vai_tro`) ON UPDATE CASCADE;

--
-- Các ràng buộc cho bảng `thanhtoan`
--
ALTER TABLE `thanhtoan`
  ADD CONSTRAINT `fk_thanhtoan_dangky` FOREIGN KEY (`ma_dang_ky`) REFERENCES `dangkygoitap` (`ma_dang_ky`) ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_thanhtoan_taikhoan` FOREIGN KEY (`ma_tai_khoan_tao`) REFERENCES `taikhoan` (`ma_tai_khoan`) ON DELETE SET NULL ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
