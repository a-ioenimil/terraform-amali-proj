from diagrams import Diagram, Cluster, Edge
from diagrams.aws.network import (
    VPC,
    InternetGateway,
    NATGateway,
    ALB,
    RouteTable,
    PublicSubnet,
    PrivateSubnet,
)
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.security import Shield
from diagrams.onprem.client import Users


def main():
    # Main diagram attributes - large canvas with generous spacing
    graph_attr = {
        "fontsize": "20",
        "bgcolor": "white",
        "pad": "2.0",
        "splines": "ortho",
        "nodesep": "1.5",
        "ranksep": "2.0",
        "fontname": "Sans-Serif",
        "labeljust": "l",
        "dpi": "150",
    }

    # Node attributes for consistent sizing
    node_attr = {
        "fontsize": "12",
        "fontname": "Sans-Serif",
    }

    # Edge attributes for cleaner lines
    edge_attr = {
        "fontsize": "10",
        "fontname": "Sans-Serif",
    }

    # Cluster styling presets
    region_style = {
        "bgcolor": "#f5f5f5",
        "style": "rounded",
        "penwidth": "2",
        "fontsize": "16",
        "fontcolor": "#333333",
        "labeljust": "l",
        "margin": "30",
    }

    vpc_style = {
        "bgcolor": "#e8f4e8",
        "style": "rounded",
        "penwidth": "2",
        "fontsize": "14",
        "fontcolor": "#1a5c1a",
        "labeljust": "l",
        "margin": "25",
    }

    az_style = {
        "bgcolor": "#f0f0ff",
        "style": "rounded,dashed",
        "penwidth": "2",
        "fontsize": "13",
        "fontcolor": "#4a4a8a",
        "margin": "20",
    }

    public_subnet_style = {
        "bgcolor": "#d4edda",
        "style": "rounded",
        "penwidth": "1.5",
        "fontsize": "11",
        "fontcolor": "#155724",
        "margin": "15",
    }

    app_subnet_style = {
        "bgcolor": "#cce5ff",
        "style": "rounded",
        "penwidth": "1.5",
        "fontsize": "11",
        "fontcolor": "#004085",
        "margin": "15",
    }

    db_subnet_style = {
        "bgcolor": "#fff3cd",
        "style": "rounded",
        "penwidth": "1.5",
        "fontsize": "11",
        "fontcolor": "#856404",
        "margin": "15",
    }

    network_components_style = {
        "bgcolor": "#e2e3e5",
        "style": "rounded",
        "penwidth": "1.5",
        "fontsize": "12",
        "fontcolor": "#383d41",
        "margin": "20",
    }

    security_style = {
        "bgcolor": "#f8d7da",
        "style": "rounded",
        "penwidth": "1.5",
        "fontsize": "12",
        "fontcolor": "#721c24",
        "margin": "20",
    }

    routing_style = {
        "bgcolor": "#d1ecf1",
        "style": "rounded",
        "penwidth": "1.5",
        "fontsize": "12",
        "fontcolor": "#0c5460",
        "margin": "20",
    }

    db_subnet_group_style = {
        "bgcolor": "#ffeeba",
        "style": "rounded",
        "penwidth": "2",
        "fontsize": "12",
        "fontcolor": "#856404",
        "margin": "15",
    }

    with Diagram(
        "AWS 3-Tier Application Architecture (eu-west-1)\nAuthor: Isaac Obo Enimil",
        show=False,
        direction="LR",
        filename="aws_3tier_architecture",
        outformat="png",
        graph_attr=graph_attr,
        node_attr=node_attr,
        edge_attr=edge_attr,
    ):
        # ========== EXTERNAL USER ==========
        internet_user = Users("Internet\nUser")

        with Cluster("AWS Region eu-west-1", graph_attr=region_style):
            with Cluster("VPC 10.0.0.0/16", graph_attr=vpc_style):

                # ========== NETWORK GATEWAY COMPONENTS ==========
                with Cluster("Network Gateways", graph_attr=network_components_style):
                    igw = InternetGateway("Internet\nGateway")
                    nat_gw_1a = NATGateway("NAT Gateway\n(eu-west-1a)")

                # ========== SECURITY GROUPS ==========
                with Cluster("Security Groups", graph_attr=security_style):
                    alb_sg = Shield("ALB SG\n(In: 80/tcp)")
                    app_sg = Shield("App SG\n(In: 80/tcp, ICMP)")
                    db_sg = Shield("DB SG\n(In: 3306/tcp)")

                # ========== ROUTE TABLES ==========
                with Cluster("Route Tables", graph_attr=routing_style):
                    rt_public = RouteTable("Public RT\n0.0.0.0/0 → IGW")
                    rt_app = RouteTable("App RT\n0.0.0.0/0 → NAT")
                    rt_db = RouteTable("DB RT\nLocal Only")

                # ========== DB SUBNET GROUP ==========
                with Cluster("DB Subnet Group", graph_attr=db_subnet_group_style):
                    db_subnet_group_label = RDS("Multi-AZ\nSubnet Group")

                # ========== AVAILABILITY ZONE 1a ==========
                with Cluster("Availability Zone: eu-west-1a", graph_attr=az_style):
                    with Cluster(
                        "Public Subnet 1a\n10.0.1.0/24", graph_attr=public_subnet_style
                    ):
                        alb_1a = ALB("Application\nLoad Balancer")

                    with Cluster(
                        "Private App Subnet 1a\n10.0.3.0/24",
                        graph_attr=app_subnet_style,
                    ):
                        ec2_app_1a = EC2("EC2 Instance\n(ASG)\nt3.micro")

                    with Cluster(
                        "Private DB Subnet 1a\n10.0.5.0/24", graph_attr=db_subnet_style
                    ):
                        rds_1a = RDS("RDS MySQL\nPrimary\ndb.t3.micro")

                # ========== AVAILABILITY ZONE 1b ==========
                with Cluster("Availability Zone: eu-west-1b", graph_attr=az_style):
                    with Cluster(
                        "Public Subnet 1b\n10.0.2.0/24", graph_attr=public_subnet_style
                    ):
                        alb_1b = ALB("Application\nLoad Balancer")

                    with Cluster(
                        "Private App Subnet 1b\n10.0.4.0/24",
                        graph_attr=app_subnet_style,
                    ):
                        ec2_app_1b = EC2("EC2 Instance\n(ASG)\nt3.micro")

                    with Cluster(
                        "Private DB Subnet 1b\n10.0.6.0/24", graph_attr=db_subnet_style
                    ):
                        rds_1b = RDS("RDS MySQL\nStandby\ndb.t3.micro")

                # ===== PRIMARY TRAFFIC FLOW (Internet → ALB → EC2 → RDS) =====

                # Internet User to Internet Gateway
                (
                    internet_user
                    >> Edge(
                        label="HTTPS/HTTP",
                        color="#28a745",
                        penwidth="2.5",
                        fontcolor="#28a745",
                    )
                    >> igw
                )

                # Internet Gateway to ALBs
                (
                    igw
                    >> Edge(
                        label="HTTP 80",
                        color="#28a745",
                        penwidth="2",
                        fontcolor="#28a745",
                    )
                    >> alb_1a
                )

                (
                    igw
                    >> Edge(
                        label="HTTP 80",
                        color="#28a745",
                        penwidth="2",
                        fontcolor="#28a745",
                    )
                    >> alb_1b
                )

                # ALB to EC2 instances (cross-AZ load balancing)
                (
                    alb_1a
                    >> Edge(
                        label="HTTP 80",
                        color="#007bff",
                        penwidth="2",
                        fontcolor="#007bff",
                    )
                    >> ec2_app_1a
                )

                (
                    alb_1a
                    >> Edge(
                        color="#007bff",
                        penwidth="1.5",
                        style="dashed",
                    )
                    >> ec2_app_1b
                )

                (
                    alb_1b
                    >> Edge(
                        label="HTTP 80",
                        color="#007bff",
                        penwidth="2",
                        fontcolor="#007bff",
                    )
                    >> ec2_app_1b
                )

                (
                    alb_1b
                    >> Edge(
                        color="#007bff",
                        penwidth="1.5",
                        style="dashed",
                    )
                    >> ec2_app_1a
                )

                # EC2 to RDS (database connections)
                (
                    ec2_app_1a
                    >> Edge(
                        label="MySQL 3306",
                        color="#fd7e14",
                        penwidth="2",
                        fontcolor="#fd7e14",
                    )
                    >> rds_1a
                )

                (
                    ec2_app_1a
                    >> Edge(
                        color="#fd7e14",
                        penwidth="1.5",
                        style="dashed",
                    )
                    >> rds_1b
                )

                (
                    ec2_app_1b
                    >> Edge(
                        label="MySQL 3306",
                        color="#fd7e14",
                        penwidth="2",
                        fontcolor="#fd7e14",
                    )
                    >> rds_1b
                )

                (
                    ec2_app_1b
                    >> Edge(
                        color="#fd7e14",
                        penwidth="1.5",
                        style="dashed",
                    )
                    >> rds_1a
                )

                # ===== OUTBOUND TRAFFIC (EC2 → NAT → IGW) =====
                (
                    ec2_app_1a
                    >> Edge(
                        label="Outbound",
                        color="#6c757d",
                        penwidth="1.5",
                        style="dashed",
                        fontcolor="#6c757d",
                    )
                    >> nat_gw_1a
                )

                (
                    ec2_app_1b
                    >> Edge(
                        color="#6c757d",
                        penwidth="1.5",
                        style="dashed",
                    )
                    >> nat_gw_1a
                )

                (
                    nat_gw_1a
                    >> Edge(
                        label="0.0.0.0/0",
                        color="#6c757d",
                        penwidth="1.5",
                        style="dashed",
                        fontcolor="#6c757d",
                    )
                    >> igw
                )

                # ===== DB SUBNET GROUP MEMBERSHIP =====
                (
                    rds_1a
                    - Edge(
                        label="member",
                        color="#fd7e14",
                        style="dotted",
                        penwidth="1.5",
                    )
                    - db_subnet_group_label
                )

                (
                    rds_1b
                    - Edge(
                        label="member",
                        color="#fd7e14",
                        style="dotted",
                        penwidth="1.5",
                    )
                    - db_subnet_group_label
                )

                # ===== SECURITY GROUP ASSOCIATIONS =====
                alb_1a - Edge(color="#dc3545", style="dotted", penwidth="1") - alb_sg
                alb_1b - Edge(color="#dc3545", style="dotted", penwidth="1") - alb_sg
                (
                    ec2_app_1a
                    - Edge(color="#dc3545", style="dotted", penwidth="1")
                    - app_sg
                )
                (
                    ec2_app_1b
                    - Edge(color="#dc3545", style="dotted", penwidth="1")
                    - app_sg
                )
                rds_1a - Edge(color="#dc3545", style="dotted", penwidth="1") - db_sg
                rds_1b - Edge(color="#dc3545", style="dotted", penwidth="1") - db_sg

                # ===== ROUTE TABLE ASSOCIATIONS =====
                alb_1a - Edge(color="#17a2b8", style="dotted", penwidth="1") - rt_public
                alb_1b - Edge(color="#17a2b8", style="dotted", penwidth="1") - rt_public
                (
                    ec2_app_1a
                    - Edge(color="#17a2b8", style="dotted", penwidth="1")
                    - rt_app
                )
                (
                    ec2_app_1b
                    - Edge(color="#17a2b8", style="dotted", penwidth="1")
                    - rt_app
                )
                rds_1a - Edge(color="#17a2b8", style="dotted", penwidth="1") - rt_db
                rds_1b - Edge(color="#17a2b8", style="dotted", penwidth="1") - rt_db

    print("Diagram generated: aws_3tier_architecture.png")


if __name__ == "__main__":
    main()
