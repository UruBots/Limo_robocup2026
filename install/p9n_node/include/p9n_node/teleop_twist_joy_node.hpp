// Copyright 2022 HarvestX Inc.
// (etc...)

#pragma once

#include <string>
#include <memory>
#include <sensor_msgs/msg/joy.hpp>
#include <geometry_msgs/msg/twist.hpp>
#include <rclcpp/rclcpp.hpp>
#include <std_msgs/msg/empty.hpp>  // Para a mensagem de gatilho

#include <p9n_interface/p9n_interface.hpp>


namespace p9n_node
{
// (Esta é a ÚNICA definição da classe)
class TeleopTwistJoyNode : public rclcpp::Node
{
public:
  using Twist = geometry_msgs::msg::Twist;
  using Joy = sensor_msgs::msg::Joy;
  using Empty = std_msgs::msg::Empty;

private:
  double linear_max_speed_, angular_max_speed_;

  p9n_interface::HW_TYPE hw_type_;
  std::unique_ptr<p9n_interface::PlayStationInterface> p9n_if_;

  rclcpp::Subscription<Joy>::SharedPtr joy_sub_;
  rclcpp::Publisher<Twist>::SharedPtr twist_pub_;
  rclcpp::Publisher<Empty>::SharedPtr save_map_pub_; // Publisher do gatilho

  rclcpp::TimerBase::SharedPtr timer_watchdog_;

  // --- NOSSAS VARIÁVEIS DE CONTROLE ---
  int prev_r1_state_{0};  // Do R1
  int prev_r2_state_{0};  // Do R2
  int prev_x_state_{0};   // Do botão X

public:
  TeleopTwistJoyNode() = delete;
  explicit TeleopTwistJoyNode(const rclcpp::NodeOptions & options);
  void onJoy(Joy::ConstSharedPtr joy_msg);
  void onWatchdog();
};
}  // namespace p9n_node
