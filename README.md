# FailSafeVM

Predicting Virtual Machine failure due to hardware/software faults by analyzing the host logs, hypervisor logs and server resource usage data in real-time using a machine learning-based approach.

## Table of Contents
1. [Introduction](#introduction)
2. [Research gap](#research-gap)
3. [Implementation](#implementation)
4. [Technologies](#technologies)
5. [Novelty](#novelty)
6. [References](#references)


## Introduction

A Virtual Machine (VM) is a software emulation of a physical computer. VMs are complex systems, and they are prone to failure (Nam et al., 2021). The focus of this project is on VM failures due to Out-of-memory and Hard Disk Drive errors. VM and (Physical Machine) PM failures are signaled by several indicators (Nam et al., 2021).
- Resource usage data
- Sensor data 
- System log data

These signals can be analyzed to predict VM and PM failures. If VM failures can be predicted below mentioned fault tolerance approaches can be used to save VMs from failing (Alam et al., 2020).
- Live migration
- System rejuvenation
- Software rejuvenation

## Research gap

- Limited use of heterogeneous data: The existing studies primarily focuses on using either VM and PM logs or PM resource usage data for predicting VM failures, overlooking the potential benefits of integrating system logs and resource usage data for more accurate and timely predictions. (Nam, Yoo and Hong, 2022; Saxena and Singh, 2022).

- Failure to perform log analysis: The studies that have used heterogeneous data, such as system logs and resource usage data, do not analyze these logs. Instead, they count the number of log events (Lin et al., 2018).

- Being VM specific: The existing studies in this research domain have been constrained to predicting failures of a specific VM rather than generalizing the prediction to cater to a wide range of PMs and VMs (Jeong et al., 2021).

## Implementation

Various temporal signals, such as performance counters, logs, and OS events, signal VM failures (pre-failure signals). Typically, in a failure scenario of a VM, these monitoring data contain both failure-related and benign data. An anomaly detection-based approach was used to identify anomalies in prediction data. Anomaly detection on log data and resource data was conducted separately and then combined to calculate the VM failure probability.

### Anomaly Detection: System Logs
The system logs were preprocessed using the Drain parser. It converts raw log messages into log keys. Log keys are numerical representations of the log messages. An LSTM-based model was used to detect anomalies in log data. It uses a window of 10 previous log keys as input. The model was trained only on benign data.

### Anomaly Detection: Resource Usage
The resource usage data was preprocessed using Minmax scaling. An NN-based autoencoder model was implemented for anomaly detection. The model uses a window of 10 resource data metrics as input. The model was trained only on benign data.

### Technologies

- Python
- Flask
- Tensorflow
- JavaScript
- React
- HTML
- CSS
- Vmstat

[![Built with](https://skillicons.dev/icons?i=python,tensorflow,flask,ubuntu,bash,javascript,react,html,css,redhat)](/)

## Novelty

A novel approach:  The implemented system uses a novel approach to predict VM failures using a combination of system log data and resource usage data.

A novel methodology: The system uses a novel methodology for detecting anomalies in system log and resource usage data using a combination of an LSTM model and an NN-based autoencoder model.

Increasing the time for prevention: The implemented methodology is able to predict OOM and HDD failures earlier than single input-based models.

## References

- Alam, A.B.M.B. et al. (2020). Optimizing Virtual Machine Migration in Multi-Clouds. 2020 International Symposium on Networks, Computers and Communications (ISNCC). 20 October 2020. Montreal, QC, Canada: IEEE, 1–7. Available from https://doi.org/10.1109/ISNCC49221.2020.9297318 [Accessed 23 September 2023].

- Du, M. et al. (2017). DeepLog: Anomaly Detection and Diagnosis from System Logs through Deep Learning. Proceedings of the 2017 ACM SIGSAC Conference on Computer and Communications Security. 30 October 2017. Dallas Texas USA: ACM, 1285–1298. Available from https://doi.org/10.1145/3133956.3134015 [Accessed 27 March 2024].

- Jeong, S. et al. (2021). Proactive Live Migration for Virtual Network Functions using Machine Learning. 2021 17th International Conference on Network and Service Management (CNSM). 25 October 2021. Izmir, Turkey: IEEE, 335–339. Available from https://doi.org/10.23919/CNSM52442.2021.9615564 [Accessed 25 September 2023].

- Lin, Q. et al. (2018). Predicting Node failure in cloud service systems. Proceedings of the 2018 26th ACM Joint Meeting on European Software Engineering Conference and Symposium on the Foundations of Software Engineering. 26 October 2018. Lake Buena Vista FL USA: ACM, 480–490. Available from https://doi.org/10.1145/3236024.3236060 [Accessed 23 September 2023].

- Nam, S. et al. (2021). Virtual Machine Failure Prediction using Log Analysis. 2021 22nd Asia-Pacific Network Operations and Management Symposium (APNOMS). 8 September 2021. Tainan, Taiwan: IEEE, 279–284. Available from https://doi.org/10.23919/APNOMS52696.2021.9562588 [Accessed 23 September 2023].

- Nam, S., Yoo, J.-H. and Hong, J.W.-K. (2022). VM Failure Prediction with Log Analysis using BERT-CNN Model. 2022 18th International Conference on Network and Service Management (CNSM). 31 October 2022. Thessaloniki, Greece: IEEE, 331–337. Available from https://doi.org/10.23919/CNSM55787.2022.9965187 [Accessed 25 September 2023].

- Saxena, D. and Singh, A.K. (2022). VM Failure Prediction based Intelligent Resource Management Model for Cloud Environments. 2022 Second International Conference on Power, Control and Computing Technologies (ICPC2T). 1 March 2022. Raipur, India: IEEE, 1–6. Available from https://doi.org/10.1109/ICPC2T53885.2022.9777020 [Accessed 25 September 2023].

- BERT Language Model. International Journal of Advanced Computer Science and Applications, 14 (6). Available from https://doi.org/10.14569/IJACSA.2023.0140675 [Accessed 19 November 2023].

- Georgoulopoulos, N. et al. (2021). Investigation and Simulation of Hardware Errors in Kernel Logs of Linux-based Server Systems. 2021 6th South-East Europe Design Automation, Computer Engineering, Computer Networks and Social Media Conference (SEEDA-CECNSM). 24 September 2021. Preveza, Greece: IEEE, 1–7. Available from https://doi.org/10.1109/SEEDA-CECNSM53056.2021.9566232 [Accessed 2 April 2024].

- Girish, L. and Rao, S.K.N. (2023). Anomaly detection in cloud environment using artificial intelligence techniques. Computing, 105 (3), 675–688. Available from https://doi.org/10.1007/s00607-021-00941-x.

- Jeong, S. et al. (2021). Proactive Live Migration for Virtual Network Functions using Machine Learning. 2021 17th International Conference on Network and Service Management (CNSM). 25 October 2021. Izmir, Turkey: IEEE, 335–339. Available from https://doi.org/10.23919/CNSM52442.2021.9615564 [Accessed 25 September 2023].

- Li, Y. et al. (2020). Predicting Node Failures in an Ultra-Large-Scale Cloud Computing Platform: An AIOps Solution. ACM Transactions on Software Engineering and Methodology, 29 (2), 1–24. Available from https://doi.org/10.1145/3385187.

