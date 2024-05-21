# **Automated Data Analysis System**

## Requirements

- OpenStack clients 6.3.x ([Installation instructions](https://docs.openstack.org/newton/user-guide/common/cli-install-openstack-command-line-clients.html)).

  > Note: Please ensure the following OpenStack clients are installed: `python-cinderclient`, `python-keystoneclient`, `python-magnumclient`, `python-neutronclient`, `python-novaclient`, `python-octaviaclient`. See: [Install the OpenStack client](https://docs.openstack.org/newton/user-guide/common/cli-install-openstack-command-line-clients.html).

- JQ 1.6.x ([Installation instructions](https://jqlang.github.io/jq/download/)).

- Kubectl 1.26.8 ([Installation instructions](https://kubernetes.io/docs/tasks/tools/)).

- Helm 3.6.3 ([Installation instructions](https://helm.sh/docs/intro/install/)).

- MRC project with enough resources to create a Kubernetes cluster.

- Connect to [Campus network](https://studentit.unimelb.edu.au/wifi-vpn#uniwireless) if on-campus or [UniMelb Student VPN](https://studentit.unimelb.edu.au/wifi-vpn#vpn) if off-campus

## Connect to The Cluster

```
source ./unimelb-comp90024-2024-grp-66-openrc.sh
```

From one terminal (A):

```shell
ssh -i <path-to-private-key> -L 6443:$(openstack coe cluster show elastic -f json | jq -r '.master_addresses[]'):6443 ubuntu@$(openstack server show bastion -c addresses -f json | jq -r '.addresses["qh2-uom-internal"][]')
```

From **another** terminal (B):

```sh
kubectl port-forward service/elasticsearch-master -n elastic 9200:9200 
```

From the **third** terminal (C):

```sh
kubectl port-forward service/kibana-kibana -n elastic 5601:5601
```

From the **fourth** terminal (D):

```sh
kubectl port-forward service/router -n fission 9090:80
```

Test connection:

```sh
curl -k 'https://127.0.0.1:9200/_cluster/health' --user 'elastic:elastic' | jq '.' 
```

# File Directory

```
├─Archive
├─backend
│  ├─adddata
│  ├─bomquery
│  ├─concat
│  ├─index
│  ├─mharvester
│  ├─mpreprocess
│  ├─mquery
│  ├─sa2
│  ├─sa2bulk
│  └─sentiment
├─docs
└─geo
```

- `Archive` contain “scratch” or experimental files created during development
- `backend` contains all functions and packages deployed on cloud
- `docs` contains the report and the API document
- `geo` contains geographical data we use in the project

# Run

- To explore the front end, please open and run the `frontend.ipynb` after port forwarding
- To explore back end APIs, please view the [API Documentation](https://github.com/chris0311/COMP90024-Project2/blob/main/docs/API%20Document.md) after port forwarding

# Contributors

- `chris0311`: Chris Liang 1159696
- `ChrisQian6`: Cheng Qian 1266297
- `HxLu03`: Haoxuan Lu 1157489
- `stayinthistime`: Sheng Liu 1352368
- `MoonCakeRabbit`: Jingjun Hao 1365178

