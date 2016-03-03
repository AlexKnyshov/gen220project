#ifndef TABLE_H
#define TABLE_H
#include <QAbstractTableModel>
#include <QBrush>
#include <QTimer>

class MyModel : public QAbstractTableModel
{
    Q_OBJECT
public:
    MyModel(QObject *parent);
    int rowCount(const QModelIndex &parent = QModelIndex()) const ;
    int columnCount(const QModelIndex &parent = QModelIndex()) const;
    QVariant data(const QModelIndex &index, int role = Qt::DisplayRole) const;
    bool setData(const QModelIndex & index, const QVariant & value, int role = Qt::EditRole);
    Qt::ItemFlags flags(const QModelIndex & index) const ;
    QTimer *timer;
signals:
    void editCompleted(const QString &);
private slots:
    void timerHit();
};
#endif // TABLE_H
