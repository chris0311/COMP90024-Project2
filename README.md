# Connecting to Cloud Clusters

## Pre-requirements

- OpenStack clients 6.3.x ([Installation instructions](https://docs.openstack.org/newton/user-guide/common/cli-install-openstack-command-line-clients.html)).

  > Note: Please ensure the following Openstack clients are installed: `python-cinderclient`, `python-keystoneclient`, `python-magnumclient`, `python-neutronclient`, `python-novaclient`, `python-octaviaclient`. See: [Install the OpenStack client](https://docs.openstack.org/newton/user-guide/common/cli-install-openstack-command-line-clients.html).

- JQ 1.6.x ([Installation instructions](https://jqlang.github.io/jq/download/)).

- Kubectl 1.26.8 ([Installation instructions](https://kubernetes.io/docs/tasks/tools/)).

- Helm 3.6.3 ([Installation instructions](https://helm.sh/docs/intro/install/)).

- MRC project with enough resources to create a Kubernetes cluster.

- Connect to [Campus network](https://studentit.unimelb.edu.au/wifi-vpn#uniwireless) if on-campus or [UniMelb Student VPN](https://studentit.unimelb.edu.au/wifi-vpn#vpn) if off-campus

## Connect to Elastic Search

```
source ./<your project name>-openrc.sh 
```

From one terminal (A):

```shell
ssh -i <path-to-private-key> (e.g. ~/Downloads/mykeypair.pem) -L 6443:$(openstack coe cluster show elastic -f json | jq -r '.master_addresses[]'):6443 ubuntu@$(openstack server show bastion -c addresses -f json | jq -r '.addresses["qh2-uom-internal"][]')
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

Test connection:

```sh
curl -k 'https://127.0.0.1:9200/_cluster/health' --user 'elastic:elastic' | jq '.' 
```

