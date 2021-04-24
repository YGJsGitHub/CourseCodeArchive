#!/usr/bin/env python
# coding: utf-8

# In[65]:


import  torch
from    torch import  nn
from    torch.nn import functional as F


# In[66]:


class ResBlk(nn.Module):
    """
    resnet block
    """

    def __init__(self, ch_in, ch_out, stride=1):
        """
        :param ch_in:
        :param ch_out:
        """
        super(ResBlk, self).__init__()

        self.conv1 = nn.Conv2d(ch_in, ch_out, kernel_size=3, stride=stride, padding=1)
        self.bn1 = nn.BatchNorm2d(ch_out)
        self.conv2 = nn.Conv2d(ch_out, ch_out, kernel_size=3, stride=1, padding=1)
        self.bn2 = nn.BatchNorm2d(ch_out)
        
        #self.extra = nn.Sequential()
        #if ch_out != ch_in:
        #    # [b, ch_in, h, w] => [b, ch_out, h, w]
        self.extra = nn.Sequential(
            nn.Conv2d(ch_in, ch_out, kernel_size=1, stride=stride),
            nn.BatchNorm2d(ch_out)
        )


    def forward(self, x):
        """
        :param x: [b, ch, h, w]
        :return:
        """
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        
        #out1 = F.relu(self.bn1(self.conv1(x)))
        #out2 = F.relu(self.bn2(self.conv2(out1)))
        #out3 = F.relu(self.bn3(self.conv3(out2)))
        #out  = F.relu(self.bn4(self.conv4(out3)))
        
        #print('out1的shape：',out1.shape)
        #print('out2的shape：',out2.shape)
        #print('out3的shape：',out3.shape)
        #print('out的shape：',out.shape)
        
        # short cut.
        # extra module: [b, ch_in, h, w] => [b, ch_out, h, w]
        # element-wise add:
        out = self.extra(x) + out
        out = F.relu(out)

        return out


# In[67]:


class ResNet18(nn.Module):

    def __init__(self, num_class):
        super(ResNet18, self).__init__()

        self.conv1 = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3),
            nn.BatchNorm2d(64)
        )
        self.pool = nn.Sequential(
            nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
            #nn.BatchNorm2d(64)
        )
        # followed 4 blocks
        # [b, 16, h, w] => [b, 32, h ,w]
        self.blk1 = ResBlk(64, 64, stride=1)
        self.blk2 = ResBlk(64, 64, stride=1)
        # [b, 32, h, w] => [b, 64, h, w]
        self.blk3 = ResBlk(64, 128, stride=2)
        self.blk4 = ResBlk(128, 128, stride=1)
        # # [b, 64, h, w] => [b, 128, h, w]
        self.blk5 = ResBlk(128, 256, stride=2)
        self.blk6 = ResBlk(256, 256, stride=1)        
        # # [b, 128, h, w] => [b, 256, h, w]
        self.blk7 = ResBlk(256, 512, stride=2)
        self.blk8 = ResBlk(512, 512, stride=1)

        # [b, 256, 7, 7]
        self.outlayer = nn.Linear(512*7*7, num_class)

    def forward(self, x):
        """
        :param x:
        :return:
        """
        x = F.relu(self.conv1(x))
        x = self.pool(x)
        #print('经过conv1时x的shape：',x.shape)
        # [b, 64, h, w] => [b, 1024, h, w]
        x = self.blk1(x)
        x = self.blk2(x)
        #print('经过blk1时x的shape：',x.shape)
        x = self.blk3(x)
        x = self.blk4(x)
        #print('经过blk2时x的shape：',x.shape)
        x = self.blk5(x)
        x = self.blk6(x)
        #print('经过blk3时x的shape：',x.shape)
        x = self.blk7(x)
        x = self.blk8(x)
        #print('经过blk4时x的shape：',x.shape)
        
        x = x.view(x.size(0), -1)
        x = self.outlayer(x)


        return x


# In[68]:


def main():
    blk = ResBlk(64, 128)
    tmp = torch.randn(2, 64, 224, 224)
    out = blk(tmp)
    print('block:', out.shape)


    model = ResNet18(7)
    tmp = torch.randn(2, 3, 224, 224)
    out = model(tmp)
    print('resnet:', out.shape)

    p = sum(map(lambda p:p.numel(), model.parameters()))
    print('parameters size:', p)


# In[69]:


if __name__ == '__main__':
    main()