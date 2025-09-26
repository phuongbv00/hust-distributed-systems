import java.util.concurrent.TimeUnit;
import java.util.concurrent.locks.ReentrantLock;


class ResourcesExploiter {
    private int rsc;

    public ResourcesExploiter(int n) {
        this.rsc = n;
    }

    public void setRsc(int n) {
        this.rsc = n;
    }

    public int getRsc() {
        return this.rsc;
    }

    public void exploit() {
        setRsc(getRsc() + 1);
    }
}


class ThreadedWorkerWithoutSync extends Thread {
    private ResourcesExploiter rExp;

    public ThreadedWorkerWithoutSync(ResourcesExploiter rExp) {
        this.rExp = rExp;
    }

    @Override
    public void run() {
        for (int i = 0; i < 1000; i++) {
            rExp.exploit();
        }
    }
}


class ThreadedWorkerWithSync extends Thread {
    private ResourcesExploiter rExp;

    public ThreadedWorkerWithSync(ResourcesExploiter rExp) {
        this.rExp = rExp;
    }

    @Override
    public void run() {
        synchronized (rExp) {
            for (int i = 0; i < 1000; i++) {
                rExp.exploit();
            }
        }
    }
}


class ResourcesExploiterWithLock extends ResourcesExploiter {
    private ReentrantLock lock;

    public ResourcesExploiterWithLock(int n) {
        super(n);
        lock = new ReentrantLock();
    }

    @Override
    public void exploit() {
        try {
            if (lock.tryLock(10, TimeUnit.SECONDS)) {
                setRsc(getRsc() + 1);
            }
        } catch (InterruptedException e) {
            e.printStackTrace();
        } finally {
            if (lock.isHeldByCurrentThread()) {
                lock.unlock();
            }
        }
    }
}


class ThreadedWorkerWithLock extends Thread {
    private ResourcesExploiterWithLock rExp;

    public ThreadedWorkerWithLock(ResourcesExploiterWithLock rExp) {
        this.rExp = rExp;
    }

    @Override
    public void run() {
        for (int i = 0; i < 1000; i++) {
            rExp.exploit();
        }
    }
}


public class Main {

    public static void main(String[] args) {
        System.out.println("runWithoutSync:");
        runWithoutSync();
        System.out.println("runWithSync:");
        runWithSync();
        System.out.println("runWithLock:");
        runWithLock();
    }

    public static void runWithoutSync() {
        ResourcesExploiter resource = new ResourcesExploiter(0);

        ThreadedWorkerWithoutSync worker1 = new ThreadedWorkerWithoutSync(resource);
        ThreadedWorkerWithoutSync worker2 = new ThreadedWorkerWithoutSync(resource);
        ThreadedWorkerWithoutSync worker3 = new ThreadedWorkerWithoutSync(resource);

        worker1.start();
        worker2.start();
        worker3.start();

        try {
            worker1.join();
            worker2.join();
            worker3.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        System.out.println("Giá trị cuối cùng của resource: " + resource.getRsc());
    }


    public static void runWithSync() {
        ResourcesExploiter resource = new ResourcesExploiter(0);

        ThreadedWorkerWithSync worker1 = new ThreadedWorkerWithSync(resource);
        ThreadedWorkerWithSync worker2 = new ThreadedWorkerWithSync(resource);
        ThreadedWorkerWithSync worker3 = new ThreadedWorkerWithSync(resource);

        worker1.start();
        worker2.start();
        worker3.start();

        try {
            worker1.join();
            worker2.join();
            worker3.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        System.out.println("Giá trị cuối cùng của resource: " + resource.getRsc());
    }


    public static void runWithLock() {
        ResourcesExploiterWithLock resource = new ResourcesExploiterWithLock(0);

        ThreadedWorkerWithLock worker1 = new ThreadedWorkerWithLock(resource);
        ThreadedWorkerWithLock worker2 = new ThreadedWorkerWithLock(resource);
        ThreadedWorkerWithLock worker3 = new ThreadedWorkerWithLock(resource);

        worker1.start();
        worker2.start();
        worker3.start();

        try {
            worker1.join();
            worker2.join();
            worker3.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        System.out.println("Giá trị cuối cùng của resource: " + resource.getRsc());
    }
}
