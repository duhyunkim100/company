from django.shortcuts import render
from networkapp.models import Company, Transaction
from django.http import HttpResponse
import io
import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.font_manager as fm
from django.http import JsonResponse


#  **기업 검색 함수**
def search_company(request):
    if request.method == "POST":
        search_text = request.POST.get("search_text", "").strip()
        related_companies = Company.objects.filter(
            name__icontains=search_text
        ) | Company.objects.filter(
            category__icontains=search_text
        ) | Company.objects.filter(
            main_product__icontains=search_text
        )

        if not related_companies:
            return render(request, "search.html", {"error": "검색 결과가 없습니다."})

        return render(request, "result.html", {"search_text": search_text, "companies": related_companies})

    return render(request, "search.html")


def network_view(request, company_name):
    """네트워크 데이터를 amCharts 형식으로 변환하여 템플릿에 전달"""
    
    print(f"[DEBUG] 네트워크 뷰 호출됨: company_name={company_name}")
    
    # 트랜잭션 데이터 조회
    transactions = Transaction.objects.filter(company__name=company_name) | \
                  Transaction.objects.filter(partner__name=company_name)
    
    if not transactions.exists():
        # 빈 데이터 반환
        empty_data = {
            "name": company_name,
            "value": 0,
            "children": []
        }
        return render(request, 'network.html', {
            'company_name': company_name,
            'network_data': empty_data
        })
    
    # 기존 방식으로 노드와 엣지 데이터 계산
    nodes = {}
    edges = []
    
    for transaction in transactions:
        company = transaction.company.name
        partner = transaction.partner.name
        relation_type = transaction.transaction_type
        
        # "구매처 1", "구매처 2" → "구매처"로 통합
        if "구매처" in relation_type:
            relation_type = "구매처"
            color = "blue"
        elif "판매처" in relation_type:
            relation_type = "판매처"
            color = "red"
        
        # 노드 추가
        if company not in nodes:
            nodes[company] = {
                'id': company,
                'name': company,
                'label': f"{company}\n({transaction.company.category})",
                'category': transaction.company.category,
                'group': 'company'
            }
        
        if partner not in nodes:
            nodes[partner] = {
                'id': partner,
                'name': partner,
                'label': f"{partner}\n({transaction.partner.category})",
                'category': transaction.partner.category,
                'group': 'partner'
            }
        
        # 엣지 추가
        edges.append({
            'from': company,
            'to': partner,
            'color': color,
            'label': relation_type
        })
    
    # amCharts 형식으로 데이터 변환
    center_node = {
        'name': company_name,
        'value': 0,
        'children': [],
        'linkWith': []
    }
    
    # 거래 관계 노드 맵 생성
    relationship_nodes = {}
    
    # 중심 노드와 연결된 엣지 처리
    for edge in edges:
        related_company = None
        is_customer = False  # 판매처인지 여부
        
        if edge['from'] == company_name:
            related_company = edge['to']
            is_customer = edge['label'] == '판매처'
        elif edge['to'] == company_name:
            related_company = edge['from']
            is_customer = edge['label'] == '구매처'
        
        if related_company:
            # 이미 추가된 노드가 아니라면 링크위드 배열에 추가
            if related_company not in relationship_nodes:
                relationship_nodes[related_company] = True
                center_node['linkWith'].append(related_company)
            
            # 관련 노드 생성
            node_data = nodes[related_company]
            child_node = {
                'name': node_data['name'],
                'value': 1,
                'category': node_data['category'],
                'group': node_data['group'],
                'color': '#e6550d' if is_customer else '#3182bd'  # 판매처는 주황색, 구매처는 파란색
            }
            
            center_node['children'].append(child_node)
    
    # 최종 네트워크 데이터 구성
    network_data = {
        'name': 'Root',
        'value': 0,
        'children': [center_node]
    }
    
    # 컨텍스트 데이터 구성
    context = {
        'company_name': company_name,
        'network_data': network_data,
        # 원래 데이터도 함께 전달 (디버깅용)
        'nodes': list(nodes.values()),
        'edges': edges
    }
    
    
    return render(request, 'network.html', context)



