#include "table.h"

MyModel::MyModel(QObject *parent)
    :QAbstractTableModel(parent)
{
}

int MyModel::rowCount(const QModelIndex & /*parent*/) const
{
   return ROWS;
}

int MyModel::columnCount(const QModelIndex & /*parent*/) const
{
    return COLS;
}

QVariant MyModel::data(const QModelIndex &index, int role) const
{
    int row = index.row();
    int col = index.column();
    switch(role){
    case Qt::DisplayRole:
        return m_gridData[index.row()][index.column()];
        break;
    case Qt::BackgroundRole:
        if (row % 10 == 0 && col % 10 == 0)
        {
            QBrush redBackground(Qt::red);
            return redBackground;
        }
        break;
    }
    return QVariant();
}
bool MyModel::setData(const QModelIndex & index, const QVariant & value, int role)
{
    if (role == Qt::EditRole)
    {
        //save value from editor to member m_gridData
        m_gridData[index.row()][index.column()] = value.toString();
        //for presentation purposes only: build and emit a joined string
        QString result;
        for(int row= 0; row < ROWS; row++)
        {
            for(int col= 0; col < COLS; col++)
            {
                result += m_gridData[row][col] + " ";
            }
        }
        //MyModel->setData( index.row(), index.column(), m_gridData[index.row()][index.column()] );
        emit editCompleted( result );
    }
    return true;
}
Qt::ItemFlags MyModel::flags(const QModelIndex & /*index*/) const
{
    return Qt::ItemIsSelectable |  Qt::ItemIsEditable | Qt::ItemIsEnabled ;
}
