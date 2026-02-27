"""API routes for balance operations."""

from decimal import Decimal
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.database import get_db

router = APIRouter()


class DepositRequest(BaseModel):
    """Request for deposit."""

    user_id: int
    amount: Decimal


class WithdrawRequest(BaseModel):
    """Request for withdraw."""

    user_id: int
    amount: Decimal


class TransferRequest(BaseModel):
    """Request for transfer."""

    from_user_id: int
    to_user_id: int
    amount: Decimal


@router.post('/deposit')
async def deposit(body: DepositRequest):
    """Add funds to user balance."""
    if body.amount <= 0:
        raise HTTPException(400, 'Amount must be positive')
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                INSERT INTO balances (user_id, amount)
                VALUES (%s, %s)
                ON CONFLICT (user_id) DO UPDATE
                SET amount = balances.amount + EXCLUDED.amount
            ''', (body.user_id, body.amount))
            cur.execute('''
                INSERT INTO transactions (user_id, amount, type)
                VALUES (%s, %s, 'deposit')
            ''', (body.user_id, body.amount))
    return {'status': 'ok', 'user_id': body.user_id}


@router.post('/withdraw')
async def withdraw(body: WithdrawRequest):
    """Withdraw funds from user balance."""
    if body.amount <= 0:
        raise HTTPException(400, 'Amount must be positive')
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                'SELECT amount FROM balances WHERE user_id = %s',
                (body.user_id,),
            )
            row = cur.fetchone()
            current = Decimal(str(row['amount'])) if row else Decimal(0)
            if current < body.amount:
                raise HTTPException(400, 'Insufficient balance')
            cur.execute('''
                UPDATE balances SET amount = amount - %s WHERE user_id = %s
            ''', (body.amount, body.user_id))
            cur.execute('''
                INSERT INTO transactions (user_id, amount, type)
                VALUES (%s, %s, 'withdraw')
            ''', (body.user_id, -body.amount))
    return {'status': 'ok', 'user_id': body.user_id}


@router.post('/transfer')
async def transfer(body: TransferRequest):
    """Transfer funds between users."""
    if body.amount <= 0:
        raise HTTPException(400, 'Amount must be positive')
    if body.from_user_id == body.to_user_id:
        raise HTTPException(400, 'Cannot transfer to yourself')
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                'SELECT amount FROM balances WHERE user_id = %s',
                (body.from_user_id,),
            )
            row = cur.fetchone()
            current = Decimal(str(row['amount'])) if row else Decimal(0)
            if current < body.amount:
                raise HTTPException(400, 'Insufficient balance')
            cur.execute('''
                UPDATE balances SET amount = amount - %s WHERE user_id = %s
            ''', (body.amount, body.from_user_id))
            cur.execute('''
                INSERT INTO balances (user_id, amount)
                VALUES (%s, %s)
                ON CONFLICT (user_id) DO UPDATE
                SET amount = balances.amount + EXCLUDED.amount
            ''', (body.to_user_id, body.amount))
            cur.execute('''
                INSERT INTO transactions (user_id, amount, type)
                VALUES (%s, %s, 'transfer_out'), (%s, %s, 'transfer_in')
            ''', (body.from_user_id, -body.amount, body.to_user_id, body.amount))
    return {
        'status': 'ok',
        'from_user_id': body.from_user_id,
        'to_user_id': body.to_user_id,
    }


@router.get('/balance/{user_id}')
async def get_balance(user_id: int):
    """Get user balance."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                'SELECT amount FROM balances WHERE user_id = %s',
                (user_id,),
            )
            row = cur.fetchone()
    if not row:
        return {'user_id': user_id, 'balance': '0.00'}
    return {'user_id': user_id, 'balance': str(row['amount'])}
