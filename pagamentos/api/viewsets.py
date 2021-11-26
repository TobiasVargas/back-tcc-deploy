from datetime import date
import mercadopago
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from backend.settings import ACCESS_TOKEN_MELI
from pagamentos.views import get_btn_pagamento
from pagamentos.models import Saldo, SolicitacaoSaque, Lancamento
from pagamentos.api.serializers import SaldoSerializer, ValorAAdicionarSerializer, SolicitacaoSaqueSerializer


class SaldoViewset(viewsets.ModelViewSet):
    queryset = Saldo.objects.all()
    serializer_class = ValorAAdicionarSerializer

    def create(self, request, *args, **kwargs):
        serializer = ValorAAdicionarSerializer(data=request.data)
        if serializer.is_valid():
            btn = get_btn_pagamento(float(serializer.data['valor']),
                                    request.user.first_name,
                                    request.user.last_name,
                                    request.user.email,
                                    'rua',
                                    'numero',
                                    'cep',
                                    '123')
            return Response({
                'btn': btn
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        lancamentos = Lancamento.objects.filter(user=request.user)
        saldo = 0
        saldo_a_aprovar = 0
        for l in lancamentos:
            if l.disponivel_em <= date.today() and not l.estornado:
                saldo = saldo + float(l.valor)
            if l.disponivel_em > date.today() and not l.estornado:
                saldo_a_aprovar = saldo_a_aprovar + float(l.valor)
        return Response({
            'user': request.user.id,
            'valor': saldo,
            'saldo_a_aprovar': saldo_a_aprovar,
        }, status=status.HTTP_200_OK)
        # print(saldo)
        #
        # self.queryset = Saldo.objects.filter(user=request.user)
        # return super().list(self, request, *args, **kwargs)

    @action(methods=['post'], detail=False)
    def inserir_saldo(self, request, *args, **kwargs):
        mp = mercadopago.MP(ACCESS_TOKEN_MELI)
        try:
            payment_info = mp.get_payment_info(request.GET.get('id', ''))
            if payment_info['status'] == 200:
                print('oi')
                saldo = Saldo.objects.filter(user=request.user).first()
                saldo.valor = float(saldo.valor) + (float(payment_info['response']['transaction_amount']) -
                                                    (float(payment_info['response']['transaction_amount']) * 0.07))
                saldo.save()
                serializer = SaldoSerializer(instance=saldo)

                lancamento = Lancamento()
                lancamento.valor = float(payment_info['response']['transaction_amount']) - (
                        float(payment_info['response']['transaction_amount']) * 0.07)
                lancamento.user = request.user
                lancamento.disponivel_em = date.today()
                lancamento.save()

                lancamentos = Lancamento.objects.filter(user=request.user)
                saldo = 0
                for l in lancamentos:
                    if l.disponivel_em <= date.today() and not l.estornado:
                        saldo = saldo + float(l.valor)
                return Response({
                    'user': request.user.id,
                    'valor': saldo
                }, status=status.HTTP_200_OK)
                # return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class SolicitacaoSaqueViewset(viewsets.ModelViewSet):
    queryset = SolicitacaoSaque.objects.all()
    serializer_class = SolicitacaoSaqueSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        self.queryset = SolicitacaoSaque.objects.filter(user=request.user)
        return super().list(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = SolicitacaoSaqueSerializer(data=request.data)
        if serializer.is_valid():
            solicitacao = SolicitacaoSaque()
            solicitacao.user = request.user
            solicitacao.mercado_pago = serializer.data['mercado_pago']
            solicitacao.valor = serializer.data['valor']
            solicitacao.save()
            serializer = SolicitacaoSaqueSerializer(instance=solicitacao)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
